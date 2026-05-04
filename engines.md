# Search Engine Routing Reference

## Engine Selection Matrix

| Intent | Primary Engine | Fallback | Max Results | Notes |
|--------|---------------|----------|-------------|-------|
| code | GitHub Search API | StackOverflow | 5 | Prefer exact code snippets |
| academic | arXiv API | Semantic Scholar | 5 | Include DOI when available |
| web_news | 元宝搜索 (online-search skill) | Brave Search | 8 | Sort by freshness |
| review | 小红书 (xiaohongshu skill) | 什么值得买 | 6 | Include user ratings |
| general | multi-search-engine skill | Brave Search | 6 | Aggregate 2-3 engines |

## Available MCP/Skill Integrations

### online-search (元宝搜索)
- Best for: Chinese content, news, current events
- Skill trigger: `online-search` skill
- Cost: Included in platform

### multi-search-engine
- Best for: General queries, international content
- Skill trigger: `multi-search-engine` skill
- Engines: 17 engines (8 domestic + 9 international)
- Cost: No API key required

### xiaohongshu
- Best for: Product reviews, lifestyle, consumer opinions
- Skill trigger: `xiaohongshu` skill
- Cost: Included in platform

### web_search (Brave)
- Best for: International content, privacy-focused
- Tool: `web_search` built-in tool
- Cost: Per-call (minimize calls)

## Cost Optimization Rules

1. **Always try `online-search` or `multi-search-engine` first** — they have no per-call cost
2. **Use `web_search` (Brave) only as fallback** — it has API cost
3. **Limit results**: Pass `count=5` or `count=6` to `web_search`, never default
4. **Batch queries**: If user asks multiple related questions, combine into one search

## Query Refinement Tips

- Remove question words: "how to", "what is", "帮我", "请问"
- Add domain context: "python" + "list comprehension" not just "list comprehension"
- For Chinese queries: try both Chinese and English versions
- For time-sensitive: add year (2025/2026) to query

## Freshness vs Accuracy Trade-off

| Scenario | Strategy |
|----------|----------|
| User asks about recent events | Prioritize freshness, lower confidence threshold |
| User asks about stable facts | Prioritize accuracy, use cache aggressively |
| User asks about code/APIs | Check version numbers, prefer official docs |
| User asks for opinions | Aggregate multiple sources, show diversity |
