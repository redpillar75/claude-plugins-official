# Kling MCP Setup & Authorization Guide

This guide walks you through obtaining Kling API credentials and completing the authorization process for the Kling MCP plugin.

## Quick Start (5 minutes)

### 1. Get Your Credentials (3 minutes)

Visit [Kling AI](https://klingai.com/) and:
1. Create an account or sign in
2. Go to API Console / Developer Settings
3. Create or view your API credentials
4. Copy your **Access Key** and **Secret Key**

### 2. Configure Claude Code (2 minutes)

In Claude Code, use `/config env` or Settings to add:
```
KLING_ACCESS_KEY=your_key_here
KLING_SECRET_KEY=your_secret_here
```

### 3. Install Plugin

```
/plugin install kling-mcp@claude-plugin-directory
```

Done! You're authorized and ready to generate videos and images.

---

## Detailed Setup Instructions

### Step-by-Step Credential Acquisition

#### For Kling AI Official Account

1. **Visit Kling AI**
   - Go to https://klingai.com/
   - Click "Sign Up" or "Login"

2. **Access API Settings**
   - Log in to your account
   - Navigate to **Account Settings** or **Developer Console**
   - Find the **API Keys** or **Credentials** section

3. **Generate API Credentials**
   - Click "Generate New Key" or "Create API Key"
   - You'll receive:
     - **Access Key** (starts with something like `sk_` or similar)
     - **Secret Key** (long alphanumeric string)

4. **Store Your Credentials Safely**
   - Copy both keys
   - Do NOT share these with anyone
   - Do NOT commit them to version control

#### For Alternative Providers (AceDataCloud, etc.)

If using an alternative Kling MCP implementation:
1. Sign up at the provider's platform
2. Navigate to API/Developer settings
3. Generate or find your authentication token
4. Use the token as instructed by that provider's documentation

### Environment Variable Configuration

#### Option 1: Claude Code UI (Easiest)

1. Open Claude Code
2. Click **Settings** ⚙️
3. Find **Environment Variables** or run `/config env`
4. Add two new variables:
   - Variable: `KLING_ACCESS_KEY` → Value: `your_access_key`
   - Variable: `KLING_SECRET_KEY` → Value: `your_secret_key`
5. Click **Save**
6. Restart Claude Code

#### Option 2: .env File (Local Development)

1. Create `.env` file in your project root:
   ```bash
   KLING_ACCESS_KEY=sk_xxxxxxxxxxxxx
   KLING_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxx
   ```

2. Load the file before running Claude:
   ```bash
   source .env
   claude
   ```

3. Add `.env` to `.gitignore`:
   ```bash
   echo ".env" >> .gitignore
   ```

#### Option 3: Terminal Export (Quick Testing)

```bash
export KLING_ACCESS_KEY="sk_xxxxxxxxxxxxx"
export KLING_SECRET_KEY="xxxxxxxxxxxxxxxxxxxxx"
claude
```

### Installing the Plugin

#### Method 1: Via `/plugin` Command

In Claude Code, type:
```
/plugin install kling-mcp@claude-plugin-directory
```

#### Method 2: Via Plugin Marketplace

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type `/plugin`
3. Select "Discover Plugins"
4. Search for "kling-mcp"
5. Click "Install"

#### Method 3: Manual Installation

If the above methods don't work:
1. Copy the plugin folder to your Claude Code plugins directory
2. Restart Claude Code
3. The plugin will be auto-discovered

### Verifying Authorization

After setup, verify everything works:

```
Test: Generate a simple image with Kling

Create a beautiful sunset image with warm colors
```

You should see Claude using Kling tools to generate the image. If you see errors:
- Check that environment variables are set: `echo $KLING_ACCESS_KEY`
- Verify credentials are correct in your Kling account
- Restart Claude Code
- Check logs for error messages

---

## Authorization Details

### What Happens During Setup

1. **Environment Variables Load** → Claude reads `KLING_ACCESS_KEY` and `KLING_SECRET_KEY`
2. **MCP Server Starts** → The Kling MCP server process launches
3. **Authentication** → Server authenticates with Kling API using your credentials
4. **Tools Registration** → All 13+ video and image generation tools become available
5. **Ready** → You can now use Kling tools in conversations

### Permission Model

- Your credentials are only used to authenticate API calls
- All requests go through Kling's secure API
- Kling's API handles user authentication and quotas
- Claude has no permanent storage of your credentials

### Security Considerations

✅ **Safe Practices:**
- Store credentials in environment variables
- Use Claude Code's built-in environment variable manager
- Rotate keys periodically
- Monitor your Kling account for unauthorized usage

❌ **Avoid:**
- Hardcoding credentials in code
- Committing `.env` to Git
- Sharing credentials with others
- Using weak or shared API keys

---

## Troubleshooting

### Problem: "Invalid credentials" or "Authorization failed"

**Causes:**
- Typo in access key or secret key
- Keys expired or revoked
- Wrong environment variable names
- Keys not properly loaded

**Solutions:**
1. Double-check your keys in Kling's API console
2. Verify exact spelling: `KLING_ACCESS_KEY` and `KLING_SECRET_KEY`
3. Ensure no leading/trailing whitespace in values
4. Regenerate keys if they're old
5. Restart Claude Code after changing variables

### Problem: "MCP server failed to start"

**Causes:**
- Node.js not installed
- Network connectivity issues
- Port conflicts
- Missing permissions

**Solutions:**
1. Verify Node.js is installed: `node --version`
2. Check internet connection
3. Check Claude Code logs for details
4. Try reinstalling the plugin
5. Restart your computer if port conflicts persist

### Problem: "Tool not found" or tools aren't available

**Causes:**
- Plugin not fully loaded
- Server initialization incomplete
- Credentials not loaded yet

**Solutions:**
1. Wait 5-10 seconds after starting Claude Code
2. Try sending another message (Claude will retry)
3. Restart Claude Code
4. Reinstall the plugin

### Problem: Rate limit errors

**Causes:**
- Exceeded Kling's API quota
- Multiple tools running simultaneously

**Solutions:**
1. Check your usage at kling.ai dashboard
2. Request quota increase from Kling support
3. Wait before retrying (usually 1 hour)

---

## Next Steps

Once authorized:

1. **Generate Your First Video**
   ```
   Create a 10-second video of a futuristic robot dancing
   ```

2. **Try Image Generation**
   ```
   Generate a landscape painting of mountains during sunrise
   ```

3. **Explore Advanced Features**
   - Video extension
   - Motion transfer
   - Lip-sync effects
   - Background removal

---

## Support

- **Kling AI Help**: https://klingai.com/help
- **API Documentation**: https://klingai.com/docs/api
- **MCP Specification**: https://modelcontextprotocol.io/
- **Claude Code Docs**: https://code.claude.com/docs
- **Report Issues**: GitHub repository issues

---

## FAQ

**Q: Is my data safe?**
A: Your credentials are only used for API authentication. Kling's API handles all data processing according to their privacy policy.

**Q: Can I use multiple API keys?**
A: You can update your environment variables to switch accounts. One set of credentials per Claude Code session.

**Q: What's my API quota?**
A: Check your Kling account dashboard to see usage limits and available quota.

**Q: How do I report a Kling API issue?**
A: Contact Kling support at their official website. Include your error messages and timestamps.

**Q: Can I use this offline?**
A: No, the Kling MCP requires internet connection to Kling's API servers.

---

Last Updated: 2026-07-06
