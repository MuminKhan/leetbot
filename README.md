# LeetBot

## About
This is a simple SlackBot that posts a daily LeetCode question via Slack. 

## Deploy
1. Head to api.slack.com to create a new OAuth key
2. Press the `Create New App` button
3. Choose `From Manifest` 
4. Copy the following manifest into the YAML section:

    ```
    _metadata:
    major_version: 1
    minor_version: 1
    display_information:
    name: LeetBot
    features:
    bot_user:
        display_name: LeetBot
        always_online: true
    oauth_config:
    scopes:
        bot:
        - channels:join
        - chat:write
    settings:
    org_deploy_enabled: false
    socket_mode_enabled: false
    token_rotation_enabled: false
    ```
5. Press `Install to Workspace` to generate the key
6. Invite the bot to the channel you wish to post in
7. Configure and deploy the bot against the channel
8. Consider cron-ing the service to run at desired interval
