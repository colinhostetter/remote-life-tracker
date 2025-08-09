# MTG Remote Life Tracker

This is a self-hosted web app intended for synchronizing life total tracking in paper Magic: the Gathering events between a phone on the players' table and a livestreaming computer running OBS somewhere else, without the two devices needing to have a wired connection and without needing to run a cloud server.

This was originally created to support streaming Pauper and Cube tournaments in New York City on [Twitch](https://www.twitch.tv/nyc_mtg/) and [YouTube](https://www.youtube.com/@nyc_mtg), but it should work for anybody who is trying to solve this same problem. Feel free to use it, and if you do, I'd love to hear about it.

Currently this is only set up to support two-player games of Magic. Theoretically you could pretty easily adapt this to support Commander or other card games, but I haven't had any reason to do that yet.

See below for instructions on using this app. It should be possible for computer-savvy but not-super-technical users to set this up on their own. If you have any questions or comments, feel free to open an issue or PR, or if you don't know what that means, feel free to just email me; my email is my first and last name at gmail.

## Setup Instructions

### 1. Set up Tailscale

To connect the phone and computer wirelessly without a cloud server, we use the VPN Tailscale to form a network between them. (Theoretically other VPNs would work for this too, but these instructions and the program assume you will use Tailscale.) As of 2025, Tailscale's free plan is completely sufficient for this usage.

-   To get started, go to https://tailscale.com/ and sign up.
-   Follow the instructions to download, install, and log into the Tailscale app on the computer you will use for streaming and on the phone you will use for life tracking.
-   The default domain names for tailnets ("tailnet" = Tailscale network) tend to be a bit hard to remember, so you can choose something more unique in the admin console: https://login.tailscale.com/admin/dns
-   You can also rename your phone/computer if Tailscale assigned them dumb or hard-to-remember names: https://login.tailscale.com/admin/machines

### 2. Install this program

Go to [this repository's releases page](https://github.com/colinhostetter/remote-life-tracker/releases) and download the latest version of this app for your operating system.

Make a folder for this app somewhere on your desktop, drag the .exe in, and open it. Your operating system may give you some grief about trying to run a file you downloaded off the internet, but I promise it's not a virus. You may also see a prompt from your firewall asking whether you want this app to be able to use the network; click allow.

When it starts, a terminal window will appear and show you the URL for the life tracker. Go ahead and try to open that URL on your phone. There's a little connection indicator at the top of the screen that will be green and say "Connected" if everything's working.

I'd recommend that you just add a bookmark to your phone's browser for this URL (it will be the same every time you start the app).

### 3. Configure OBS

The final step is to actually get the life values into OBS. I have included a custom OBS script to make sure the values update snappily in the broadcast as they change, because OBS is kind of sluggish about updating text sources by default.

In OBS, go to Tools -> Scripts, then press the plus button to add a script. Navigate to the folder where you installed this app. There should be a "scripts" folder there now. Load the "update_life_totals.lua" script that's in there.

On the left side of the dialog in OBS, configure the three parameters:

-   Output Folder: Navigate to the folder where you installed this app and select the "output" subfolder that should have been created.
-   Player 1 Life Text Source: The name of the text source that you want to display player 1's life total.
-   Player 2 Life Text Source: The name of the text source that you want to display player 2's life total.

Now try adjusting the life totals on your phone again. You should see them change in OBS!

## Troubleshooting

If you can't load the life tracker:

-   Make sure your computer is connected to Tailscale (and that the app is running).
-   Make sure your phone is connected to Tailscale (in your VPN settings).

If the values aren't updating in OBS:

-   Make sure you chose the folder "output" in the Output Folder parameter.

If it's still not working, feel free to ask me for help.

## Contributing

This software is released under the MIT license, so you can do whatever you want with it, but if you make improvements to it feel free to open a PR and I will probably merge it.

## While You're Here

Can I interest you in [Pauper, the People's Format](https://www.decksandthecity.org/)?
