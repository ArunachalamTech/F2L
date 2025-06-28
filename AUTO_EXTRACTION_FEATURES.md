# 🎬 Auto Extraction Features for MrAK Bot

This enhancement adds powerful auto-extraction capabilities to the MrAK (MrAK Stream) project, similar to the Auto-Rename-Bot functionality but specifically designed for caption enhancement rather than file renaming.

## ✨ New Features Added

### 1. 🔍 Auto Information Extraction
- **Quality Detection**: Automatically extracts video quality (1080p, 720p, 4K, HDRip, BluRay, WEB-DL, etc.)
- **Season Detection**: Finds season numbers (S01, S02, Season 1, etc.)
- **Episode Detection**: Identifies episode numbers (E01, E02, EP01, etc.)

### 2. 📝 Enhanced Caption System
- **New Placeholders**: Added `{quality}`, `{season}`, and `{episode}` placeholders
- **Smart Replacement**: Automatically replaces placeholders with extracted information
- **Backward Compatible**: All existing placeholders still work

### 3. ⚙️ User Controls
- **Toggle Feature**: Users can enable/disable auto extraction via `/extract` command
- **Settings Integration**: Auto extraction setting added to the settings menu
- **Per-User Setting**: Each user can have their own preference

### 4. 🎯 Testing & Examples
- **Test Command**: `/test filename` to see what information can be extracted
- **Examples Command**: `/examples` to see sample captions with new placeholders
- **Live Preview**: Real-time testing of extraction patterns

## 📋 New Commands Added

| Command | Description |
|---------|-------------|
| `/extract` or `/autoextract` | Toggle auto extraction on/off |
| `/examples` or `/example` | View caption examples with new placeholders |
| `/test filename` | Test extraction on a specific filename |

## 🔧 Technical Implementation

### Files Created/Modified:

1. **New File**: `MrAKTech/tools/extract_info.py`
   - Contains all extraction logic
   - Pattern matching for quality, season, episode detection
   - Placeholder replacement functions

2. **Modified**: `MrAKTech/database/u_db.py`
   - Added `auto_extract` field to user schema
   - Added methods to get/set auto extraction preference

3. **Modified**: `MrAKTech/plugins/stream.py`
   - Integrated extraction functionality for private messages
   - Automatic placeholder replacement in captions

4. **Modified**: `MrAKTech/plugins/channels.py`
   - Added extraction support for channel messages
   - Channel-specific caption processing

5. **Modified**: `MrAKTech/plugins/commands.py`
   - Added new commands for managing extraction features
   - Test and example commands

6. **Modified**: `MrAKTech/plugins/callback.py`
   - Added callback handlers for new features
   - Settings menu integration
   - Updated caption validation

7. **Modified**: `MrAKTech/tools/txt.py`
   - Updated help text with new commands
   - Added new placeholders to caption documentation
   - Enhanced settings display

## 🎯 Supported File Patterns

### Quality Detection:
- `1080p`, `720p`, `480p`, `4K`, `2K`
- `HDRip`, `BluRay`, `WEB-DL`, `HDTV`
- `4K x264`, `4K x265`

### Season Detection:
- `S01`, `S02`, `S1`, `S2`
- `Season 1`, `Season 2`
- `[S01]`, `(S01)`

### Episode Detection:
- `E01`, `E02`, `EP01`, `EP02`
- `S01E01`, `S01EP01`
- `S01 E01`, `S01 - E01`
- Standalone episode numbers

## 📝 Usage Examples

### Basic Caption with Auto Extraction:
```
🎥 {file_name}

📺 Quality: {quality}
🎞️ Season: {season} | Episode: {episode}
📦 Size: {file_size}

📥 Download: {download_link}
🖥️ Stream: {stream_link}
```

### Compact Format:
```
📁 {file_name} [{quality}] S{season}E{episode}
📊 {file_size} | ⬇️ {download_link}
```

## 🔄 Migration Notes

- **Existing Users**: Auto extraction is enabled by default for all users
- **Existing Captions**: Will continue to work without modification
- **New Placeholders**: Only work when auto extraction is enabled
- **Fallback**: If information cannot be extracted, placeholders show "Unknown"

## 🛠️ Configuration

Users can control the auto extraction feature through:

1. **Settings Menu**: Access via bot settings
2. **Direct Command**: Use `/extract` command
3. **Per-Feature Control**: Can be enabled/disabled independently

## 🚀 Benefits

1. **Enhanced UX**: Users get richer, more informative captions automatically
2. **Time Saving**: No need to manually add quality/season/episode info
3. **Consistency**: Standardized information extraction across all content
4. **Flexibility**: Users can choose to use the feature or not
5. **Future-Proof**: Easy to add more extraction patterns as needed

## ⚠️ Important Notes

- Auto extraction works best with properly named files
- The feature respects user privacy and preferences
- No file renaming occurs - only caption enhancement
- All existing functionality remains unchanged
- Channel admins can still use custom captions with new placeholders

This implementation provides a powerful yet user-friendly way to enhance captions with automatically extracted information while maintaining full backward compatibility with existing functionality.
