# Veracode SCA Workspace Automation

This is for automating the creation of SCA workspace and its agent token.

## Reference:
1. https://docs.veracode.com/r/c_sourceclear_intro
2. https://app.swaggerhub.com/apis/Veracode/veracode-sca_agent_api_specification/3.0#/agents/createWorkspaceAgentUsingPOST
3. https://docs.veracode.com/r/c_enabling_hmac#enable-hmac-for-python-programs 
4. https://github.com/veracode/veracode-python-hmac-example

### Update:  
The auth module is no longer required since we have imported the RequestsAuthPluginVeracodeHMAC from the veracode_api_signing.plugin_requests package.

### Usage:
Before running, ensure you have the following in your environment:

 - export VERACODE_API_KEY_ID=vera01ei-<your 32-character long Veracode API KEY ID>  
 - export VERACODE_API_KEY_SECRET=vera01es-<your 128-character long Veracode API KEY SECRET>

Your Veracode API Key ID will start with 'vera01ei-' if your platform is ER. Ensure you use the correct api_base_url (refer line 168-173)


