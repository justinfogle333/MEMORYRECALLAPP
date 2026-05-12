# Technical Foundation Research Notes

## llms.txt Specification (from llmstxt.org)
- Proposed by Jeremy Howard, September 3, 2024
- Placed at root: /llms.txt
- Format: Markdown file with specific structure
- Required: H1 with project/site name
- Optional: Blockquote summary, detail sections, H2 sections with file lists
- File lists: markdown hyperlinks with optional notes
- Keep under 10KB
- UTF-8 encoding

### llms.txt Template for Moving Company:
```
# [Brand Name]

> [Brand Name] is a [type] moving company serving [areas]. We specialize in [services].

## Services
- [Service Page URL]: Description of service
- [FAQ Page URL]: Frequently asked questions about moving

## About
- [About Page URL]: Company history and team information

## Optional
- [Blog URL]: Moving tips and guides
```

## AI Crawler User-Agents (from xseek.io)

### Must Allow (Critical for GEO):
| Crawler | Company | Purpose | User-Agent |
|---------|---------|---------|------------|
| GPTBot | OpenAI | Training GPT models | GPTBot/1.1 |
| ChatGPT-User | OpenAI | ChatGPT web browsing | ChatGPT-User/1.0 |
| OAI-SearchBot | OpenAI | ChatGPT search results | OAI-SearchBot/1.0 |
| ClaudeBot | Anthropic | Claude web browsing | ClaudeBot/1.0 |
| anthropic-ai | Anthropic | Claude training | anthropic-ai/1.0 |
| Google-Extended | Google | Gemini AI training | Google-Extended/1.0 |
| PerplexityBot | Perplexity | AI search | PerplexityBot/1.0 |
| Applebot | Apple | Siri/Apple Intelligence | Applebot/1.0 |
| Applebot-Extended | Apple | Apple Intelligence | Applebot-Extended/1.0 |

### robots.txt Template for Moving Company:
```
User-agent: *
Allow: /

# Explicitly allow AI crawlers for GEO
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: https://[domain]/sitemap.xml
```

## MovingCompany Schema (from schema.org / schemantra.com)
- @type: MovingCompany (subtype of HomeAndConstructionBusiness > LocalBusiness > Organization)
- Key properties: name, url, telephone, address, areaServed, priceRange, openingHours, aggregateRating, review
- Place JSON-LD in <head> section
- Combine with FAQPage schema for FAQ sections

### MovingCompany Schema Template:
```json
{
  "@context": "https://schema.org",
  "@type": "MovingCompany",
  "name": "[Brand Name]",
  "url": "https://[domain]",
  "telephone": "[phone]",
  "logo": "https://[domain]/logo.png",
  "image": "https://[domain]/hero.jpg",
  "description": "[Description]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[street]",
    "addressLocality": "[city]",
    "addressRegion": "[state]",
    "postalCode": "[zip]",
    "addressCountry": "US"
  },
  "areaServed": {
    "@type": "Country",
    "name": "United States"
  },
  "priceRange": "$$",
  "sameAs": [
    "https://www.facebook.com/[brand]",
    "https://www.yelp.com/biz/[brand]",
    "https://www.google.com/maps/place/[brand]"
  ]
}
```

### FAQPage Schema Template:
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much does a cross-country move cost?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The average cost of a cross-country move ranges from $2,500 to $7,500..."
      }
    }
  ]
}
```

## Sources
- llmstxt.org - Official llms.txt specification
- xseek.io - AI Robots.txt Guide
- schemantra.com - MovingCompany Schema Generator
- schema.org - MovingCompany type definition
