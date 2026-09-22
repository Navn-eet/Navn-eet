from pathlib import Path

OUT = Path("assets/cards/neofetch.svg")

lines = [
    ("Name", "Navneet Verma"),
    ("Role", "Software Engineer"),
    ("Focus", "Full Stack / Backend / Infra / DevOps"),
    ("Experience", "~3 years"),
    ("Runtime", "Node.js / TypeScript / NestJS"),
    ("Frontend", "React / Next.js / Tailwind"),
    ("Data", "PostgreSQL / MongoDB / Redis"),
    ("ORM", "Drizzle ORM"),
    ("Queues", "BullMQ / Outbox / DLQ"),
    ("Systems", "Retries / Idempotency / Locks"),
    ("Caching", "Redis / Cache Invalidation"),
    ("Testing", "Jest / Unit / Integration / E2E"),
    ("Infra", "Docker / Linux / VPS / Nginx"),
    ("Network", "SSL / TLS / DNS / Reverse Proxy"),
    ("CI/CD", "GitLab CI/CD"),
    ("Integrations", "FCM / Resend / SMTP / SMS"),
    ("CMS", "Payload CMS / Fumadocs"),
    ("Projects", "SkoolSewa / WordUnscramble"),
    ("Education", "BSc Computer Science / 2027"),
]

WIDTH = 520
HEIGHT = 500

parts = [
f'''<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}"
     height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}"
     role="img"
     aria-label="Navneet Verma profile information">

<style>
  .label {{
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
    font-weight: 600;
    fill: #69B7FF;
  }}

  .value {{
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
    fill: #D7E0EA;
  }}

  .command {{
    font-family: "JetBrains Mono", monospace;
    font-size: 13px;
    fill: #7F91A5;
  }}

  .prompt {{
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
    fill: #6EE7A0;
  }}
</style>

<rect x="1" y="1"
      width="{WIDTH - 2}"
      height="{HEIGHT - 2}"
      rx="14"
      fill="#0B1118"
      stroke="#263342"/>

<circle cx="24" cy="25" r="5" fill="#FF6B6B"/>
<circle cx="42" cy="25" r="5" fill="#FFD166"/>
<circle cx="60" cy="25" r="5" fill="#6EE7A0"/>

<text x="82" y="30" class="command">
  navneet@github ~ $ neofetch
</text>

<line x1="20" y1="48" x2="{WIDTH - 20}" y2="48"
      stroke="#263342"/>

'''
]

y = 75

for i, (label, value) in enumerate(lines):
    parts.append(
f'''<text x="24" y="{y}" class="label">{label}</text>
<text x="145" y="{y}" class="value">{value}</text>
'''
    )
    y += 21

parts.append(
f'''
<text x="24" y="{y + 3}" class="prompt">
  navneet@github ~ $ _
</text>

</svg>
'''
)

OUT.write_text("".join(parts))
print(f"Generated {OUT}")
