from youtube.channel_initializer import fetch_channel_admin_list, initialize_channels_from_admins

if __name__ == "__main__":
    admins = fetch_channel_admin_list()
    initialize_channels_from_admins(admins)