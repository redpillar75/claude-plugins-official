# Kling MCP Plugin

A comprehensive Model Context Protocol (MCP) integration for Kling AI video and image generation. This plugin enables you to generate stunning AI videos, images, and apply creative effects directly from Claude using Kling's suite of professional creative tools.

## Overview

Kling AI is an advanced AI video and image generation platform that offers:
- **Video Generation**: Create videos from text descriptions or seed images
- **Multiple Models**: Support for Kling v1.0, v1.5, v1.6, and KOLORS
- **Image Generation**: Generate high-quality images with KOLORS model
- **Creative Effects**: Apply effects, lip-sync, virtual try-ons, and more
- **Video Extension**: Extend existing videos
- **Motion Transfer**: Transfer motion between videos

This plugin provides 13+ tools with full access to all Kling capabilities.

## Installation & Setup

### Step 1: Get Kling API Credentials

1. Visit [Kling AI Platform](https://klingai.com/)
2. Sign up for an account or log in if you already have one
3. Navigate to your account settings or API console
4. Generate API credentials:
   - **KLING_ACCESS_KEY**: Your API access key
   - **KLING_SECRET_KEY**: Your API secret key
5. Keep these credentials secure and private

### Step 2: Configure Environment Variables

You need to set up your Kling API credentials as environment variables. There are multiple ways to do this:

#### Option A: Claude Code Settings (Recommended)

1. Open Claude Code settings
2. Navigate to **Settings** > **Environment Variables** (or use `/config env`)
3. Add the following environment variables:
   - `KLING_ACCESS_KEY`: Your Kling API access key
   - `KLING_SECRET_KEY`: Your Kling API secret key
4. Save the settings

#### Option B: Local Environment File

Create a `.env` file in your project root:

```bash
KLING_ACCESS_KEY=your_access_key_here
KLING_SECRET_KEY=your_secret_key_here
```

Then load it in your Claude Code session or terminal.

#### Option C: Command Line

Export the variables in your terminal before running Claude Code:

```bash
export KLING_ACCESS_KEY="your_access_key_here"
export KLING_SECRET_KEY="your_secret_key_here"
```

### Step 3: Install the Plugin

1. In Claude Code, run:
   ```
   /plugin install kling-mcp@claude-plugin-directory
   ```

2. Or browse available plugins and search for "kling-mcp"

3. The plugin will automatically start the Kling MCP server with your configured credentials

## Authorization Flow

The authorization process is handled automatically once your environment variables are set:

1. **Credentials Loading**: Claude reads `KLING_ACCESS_KEY` and `KLING_SECRET_KEY` from your environment
2. **Server Initialization**: The MCP server starts with your credentials
3. **API Connection**: The server establishes a secure connection to Kling's API
4. **Tool Registration**: All 13+ Kling tools are registered and available for use
5. **Ready to Use**: You can now generate videos and images directly in Claude

## Available Tools

Once installed and authorized, you have access to:

### Video Generation
- `text_to_video`: Generate videos from text descriptions
- `image_to_video`: Create videos from images
- `video_extend`: Extend existing videos

### Image Generation
- `text_to_image`: Generate images from text prompts (KOLORS)
- `image_edit`: Edit existing images

### Advanced Features
- `lip_sync`: Add lip-sync to videos
- `motion_transfer`: Transfer motion between videos
- `remove_background`: Remove backgrounds from images
- `upscale_image`: Upscale image resolution
- `virtual_tryon`: Apply virtual clothing try-ons
- `apply_effects`: Apply creative effects to videos

## Usage Examples

### Generate a Video from Text
```
Create a 10-second video of a sunset over mountains with calm water in the foreground
```

### Generate an Image
```
Generate a photorealistic image of a futuristic city at night with neon lights
```

### Create Video from Image
```
Turn this landscape photo into a 5-second video with subtle motion
```

## Security & Best Practices

1. **Keep Credentials Private**: Never commit your API keys to version control
2. **Use Environment Variables**: Always store credentials in environment variables, not in code
3. **Rotate Keys**: Periodically rotate your API keys for security
4. **Monitor Usage**: Check your Kling account for API usage metrics
5. **.gitignore**: Ensure `.env` files are in your `.gitignore`

## Troubleshooting

### Issue: "Authorization failed" or "Invalid credentials"
**Solution**: 
- Verify your `KLING_ACCESS_KEY` and `KLING_SECRET_KEY` are correct
- Check that environment variables are properly loaded
- Ensure credentials don't have extra whitespace
- Visit Kling AI console to confirm keys are still active

### Issue: "MCP server failed to start"
**Solution**:
- Ensure Node.js and npm are installed
- Check that your system has internet connectivity
- Verify port accessibility (the MCP server uses a local port)
- Check Claude Code logs for detailed error messages

### Issue: "Tool not found" or "Service unavailable"
**Solution**:
- Restart Claude Code
- Reinstall the plugin
- Check your Kling account subscription and API quota
- Verify your Kling API credentials haven't expired

## API Rate Limits

Kling API has rate limits:
- Check your Kling account dashboard for current limits
- Implement retry logic in your workflows
- Contact Kling support for rate limit increases if needed

## Advanced Configuration

For custom configurations or alternative Kling MCP implementations:

### Alternative: AceDataCloud Kling MCP
If you prefer the AceDataCloud implementation, you can configure it in `.mcp.json`:

```json
{
  "kling-acedata": {
    "type": "http",
    "url": "http://localhost:3000",
    "headers": {
      "Authorization": "Bearer YOUR_TOKEN_HERE"
    }
  }
}
```

## Support & Resources

- **Kling AI Documentation**: https://klingai.com/docs
- **MCP Specification**: https://modelcontextprotocol.io/
- **Claude Code Docs**: https://code.claude.com/docs
- **GitHub Issues**: Report issues in the claude-plugins-official repository

## Version History

### v1.0.0 (Current)
- Initial release
- Support for mcp-kling server
- 13+ video, image, and effect tools
- Full authorization and environment variable support
- Comprehensive documentation and troubleshooting guide

## License

This plugin integrates with Kling AI's APIs. Ensure you comply with Kling AI's terms of service and licensing agreements when using this plugin.
