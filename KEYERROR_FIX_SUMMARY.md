# KeyError Fix for Auto-Extraction Feature

## Problem Identified
The bot was throwing `KeyError: 'quality'` errors because the caption formatting was using `.format()` with placeholders that weren't always available in the format dictionary.

## Root Cause
1. `smart_replace_placeholders_in_caption()` processed `{quality}`, `{season}`, `{episode}` placeholders
2. But subsequent `.format()` calls only provided basic placeholders (file_name, caption, file_size, etc.)
3. If smart replacement didn't fully process all placeholders, `.format()` would throw KeyError for missing keys

## Solution Implemented

### 1. Created `create_safe_format_dict()` Function
- **Location**: `MrAKTech/tools/extract_info.py`
- **Purpose**: Creates a complete format dictionary with ALL possible placeholders
- **Features**:
  - Includes all basic placeholders from input dictionary
  - Adds extraction placeholders (quality, season, episode) with all case variations
  - Uses `extract_combined_info()` to get best available data
  - Defaults to empty string ("") for missing values

### 2. Updated Caption Formatting Logic

#### `stream.py` Changes:
- Import `create_safe_format_dict`
- Create basic format dictionary with all standard placeholders
- Create safe format dictionary with extraction placeholders
- Use `**safe_format_dict` in both "links" and "files" caption positions

#### `channels.py` Changes:
- Import `create_safe_format_dict`
- Create separate safe format dictionaries for shortlink and direct link versions
- Use `**safe_format_dict` in both caption editing scenarios

### 3. Error Prevention Strategy
- **Before**: `c_caption.format(file_name=..., caption=..., quality=MISSING)` → KeyError
- **After**: `c_caption.format(**safe_format_dict)` → All keys present, empty string for missing values

## Testing Results
✅ Created and ran comprehensive test showing:
- Safe format dictionary contains all expected keys
- Caption formatting succeeds without KeyError
- Extraction works correctly (1080p, S01, E05 from test filename)
- Missing values show as empty strings, not errors

## Key Benefits
1. **No More KeyError**: Bot will never crash due to missing quality/season/episode placeholders
2. **Backwards Compatible**: All existing captions continue to work
3. **Smart Extraction**: Still gets best data from filename + caption
4. **Graceful Degradation**: Missing values show as empty strings
5. **User-Friendly**: No error messages for users when data can't be extracted

## Files Modified
- `MrAKTech/tools/extract_info.py` - Added `create_safe_format_dict()` function
- `MrAKTech/plugins/stream.py` - Updated caption formatting to use safe dictionaries
- `MrAKTech/plugins/channels.py` - Updated caption formatting to use safe dictionaries

## Validation
- ✅ No compilation errors
- ✅ Test script confirms KeyError prevention
- ✅ Extraction still works properly
- ✅ All existing functionality preserved
- ✅ Changes pushed to `new` branch on GitHub

## User Experience
Users will now see:
- **Before**: Bot crash with "KeyError: quality" when extraction fails
- **After**: Clean captions with empty values for missing data, no errors

This fix ensures the auto-extraction feature is robust and never causes bot failures, while maintaining all the smart extraction capabilities for files where the data can be detected.
