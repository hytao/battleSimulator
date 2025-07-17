# Google Sheets Integration Guide

## Overview
The Battle Simulator now supports loading data directly from your Google Sheets. This allows you to:
- Use your own battle data
- Easily update unit statistics and parameters
- Share battle configurations with others
- Maintain version control of your battle scenarios

## Setting Up Your Google Sheet

### 1. Sheet Structure
Your Google Sheet should follow the same structure as the default sheet:
- **Header row 1**: Title/Description (optional)
- **Header row 2**: Column categories (optional)  
- **Header row 3**: Column names (data starts here)
- **Rows 4-8**: Team A units (5 units)
- **Rows 9-13**: Empty/separator rows
- **Rows 14-18**: Team B units (5 units)

### 2. Required Columns
Make sure your sheet includes these essential columns:
- `單位` - Unit name
- `位置` - Position
- `ATK`, `DEF`, `MOB`, `HP` - Basic stats
- `atk(base)`, `def(base)`, `mob(base)`, `hp(base)` - Base stats
- `突破` - Breakthrough percentage
- Weapon data columns
- Pilot ability columns
- And all other columns as in the reference sheet

### 3. Making Your Sheet Accessible
1. Open your Google Sheet
2. Click the "Share" button (top right)
3. Under "Get link", change access to "Anyone with the link can view"
4. Copy the generated link
5. Paste this link into the simulator when prompted

## Supported URL Formats

The simulator can parse various Google Sheets URL formats:

### Standard Edit URL
```
https://docs.google.com/spreadsheets/d/1rf1uZHKJhhCQ_10qvzQkoSaD56ExFxE8SOWAxjXlwyo/edit#gid=489835885
```

### Query Parameter Format
```
https://docs.google.com/spreadsheets/d/1rf1uZHKJhhCQ_10qvzQkoSaD56ExFxE8SOWAxjXlwyo/edit?gid=489835885
```

### Sharing URL with Parameters
```
https://docs.google.com/spreadsheets/d/1rf1uZHKJhhCQ_10qvzQkoSaD56ExFxE8SOWAxjXlwyo/edit?usp=sharing&gid=489835885#gid=489835885
```

### Simple URL (uses first sheet)
```
https://docs.google.com/spreadsheets/d/1rf1uZHKJhhCQ_10qvzQkoSaD56ExFxE8SOWAxjXlwyo/edit
```

## URL Components Explained

- **Sheet ID**: The long string of characters that identifies your specific spreadsheet
- **GID**: The sheet/tab ID within the spreadsheet (defaults to 0 for the first sheet)

## Troubleshooting

### Common Issues and Solutions

1. **"無法從URL中找到工作表ID" Error**
   - Make sure you're using a Google Sheets URL, not Google Docs or other services
   - Check that the URL contains `/spreadsheets/d/` in the path

2. **"無法載入戰鬥資料" Error**
   - Verify your sheet is publicly accessible ("Anyone with the link can view")
   - Check your internet connection
   - Ensure the sheet has the correct data structure and enough rows

3. **"資料不足" Error**
   - Your sheet needs at least 14 rows of data (after the header rows)
   - Make sure you have data in the correct positions for Team A and Team B

4. **Permission Denied Errors**
   - Your sheet must be set to public access
   - Private sheets cannot be accessed by the simulator

### Getting the Correct URL

1. **From the Address Bar**: Copy the URL directly from your browser when viewing the sheet
2. **From Share Button**: Use the "Copy link" option after setting permissions
3. **Make sure to include the GID**: If you want a specific sheet/tab, make sure the GID is in the URL

## Testing Your Setup

Use the included test script to verify URL parsing:
```bash
python test_url_parsing.py
```

This will test various URL formats and ensure the parsing logic works correctly.

## Fallback to Test Mode

If your Google Sheets URL fails to load:
1. The simulator will show an error dialog
2. You can choose to continue with built-in test data
3. This allows you to still run the simulator even if your sheet has issues

## Best Practices

1. **Keep a backup**: Save a copy of the reference sheet structure before making changes
2. **Test incremental changes**: Make small changes and test to ensure they work
3. **Use descriptive unit names**: This makes the battle logs easier to follow
4. **Document your changes**: Use comments or a separate sheet to track modifications
5. **Share read-only**: Never give edit access when sharing for simulation purposes
