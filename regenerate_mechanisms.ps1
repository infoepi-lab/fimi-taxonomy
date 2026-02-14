# Read CSV and generate mechanism pages
$csv = Import-Csv "C:\Users\ERosa\Github\v4.0-infomap\mechanisms.csv"
$examples = Import-Csv "C:\Users\ERosa\Github\v4.0-infomap\examples.csv"

# Function color mapping
$colors = @{
    "Command and Control" = "#c0392b"
    "Legitimation" = "#d35400"
    "Longevity" = "#7d3c98"
    "Obfuscation" = "#2c3e50"
    "Operational Multipliers" = "#2980b9"
    "Projection Abroad" = "#16a085"
    "Sabotage" = "#922b21"
    "Spillover" = "#1a5276"
    "Suppressing Dissent" = "#6c3483"
}

foreach ($row in $csv) {
    $name = $row.mechanism
    $slug = $name.ToLower() -replace ' ', '-'
    $func = $row.function
    $funcSlug = $func.ToLower() -replace ' ', '-'
    $oneLine = $row.one_line.Trim()
    $description = $row.description.Trim()

    # Build YAML frontmatter
    $content = @"
---
title: "$name"
description: "$oneLine"
categories: [mechanism]
function: "$func"
---

::: {.function-badge}
[$func](../function/$funcSlug.qmd)
:::

$description

"@

    # Add examples if they exist
    $mechExamples = $examples | Where-Object { $_.mechanism -eq $name }
    if ($mechExamples) {
        $content += "`n## Documented Examples`n`n"
        foreach ($ex in $mechExamples) {
            $quote = $ex.quote.Trim()
            $url = $ex.URL.Trim()
            $title = $ex.title.Trim()
            if ($quote) {
                $content += "> $quote`n>`n"
                if ($url -and $title) {
                    $linkText = "[$title]($url)"
                    $content += "> — $linkText`n`n"
                } elseif ($url) {
                    $linkText = "[Source]($url)"
                    $content += "> — $linkText`n`n"
                }
            }
        }
    }

    # Write file
    $outPath = "C:\Users\ERosa\Github\v4.0-infomap\mechanisms\$slug.qmd"
    $content | Out-File -FilePath $outPath -Encoding UTF8
    Write-Host "Wrote $outPath"
}

Write-Host "`nDone generating mechanism pages"
