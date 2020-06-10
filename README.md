# AABot
A simple Discord bot written in Python using the Discord.py API
Inspired by [this guide](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-python)

### Supported Commands
List of commands supported by AABot. Some commands require special permissions. Consult your server owner for assistance.
* \<prefix>e <echo_name>
  * The echo command. If an echo exists in the Echo List (aa!elist), a specific response will be returned.
* \<PREFIX>te <echo_name> <target_channel_id>
  * Execute an echo in the target channel.
* \<prefix>elist
  * Returns a list of all possible echos.
* \<prefix>ecreate <echo_name> <echo_response
  * Creates a new echo with specified name and response. Requires permissions of server owners.
* \<prefix>mass_give_role <role_id>
  * Gives everyone except the owner and bots the specified role.
* \<prefix>mass_remove_role <role_id>
  * Takes away from everyone except the owner and bots the specified role.
* \<prefix>command_list
  * Please consult aa!command_list for more help.
