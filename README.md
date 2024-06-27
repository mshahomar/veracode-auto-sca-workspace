# Veracode SCA Workspace Automation

This is for automating the creation of SCA workspace and its agent token.

## Reference:
1. https://docs.veracode.com/r/c_sourceclear_intro
2. https://app.swaggerhub.com/apis/Veracode/veracode-sca_agent_api_specification/3.0#/agents/createWorkspaceAgentUsingPOST
3. https://docs.veracode.com/r/c_enabling_hmac#enable-hmac-for-python-programs 
4. https://github.com/veracode/veracode-python-hmac-example

### Update:  
The auth module is no longer required since we have imported the RequestsAuthPluginVeracodeHMAC from the veracode_api_signing.plugin_requests package.