from __future__ import print_function, unicode_literals
import os
from boxsdk import Client
from boxsdk.exception import BoxAPIException
from boxsdk.object.collaboration import CollaborationRole
from auth import authenticate


def run_user_example(client):
    # 'me' is a handy value to get info on the current authenticated user.
    me = client.user(user_id='me').get(fields=['login'])
    print('The email of the user is: {0}'.format(me['login']))


def upload_file(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    a_file = root_folder.upload(file_path, file_name='i-am-a-file.txt')
    try:
        print('{0} uploaded: '.format(a_file.get()['name']))
    finally:
        print('Delete i-am-a-file.txt succeeded: {0}'.format(a_file.delete()))


def update_file(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    file_v1 = root_folder.upload(file_path, file_name='file_v1.txt')
    try:
        # print 'File content after upload: {}'.format(file_v1.content())
        file_v2_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file_v2.txt')
        file_v2 = file_v1.update_contents(file_v2_path)
        # print 'File content after update: {}'.format(file_v2.content())
    finally:
        file_v1.delete()


def search_files(client):
    search_results = client.search(
        'i-am-a-file.txt',
        limit=2,
        offset=0,
        ancestor_folders=[client.folder(folder_id='0')],
        file_extensions=['txt'],
    )
    for item in search_results:
        item_with_name = item.get(fields=['name'])
        print('matching item: ' + item_with_name.id)
    else:
        print('no matching items')


def copy_item(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    a_file = root_folder.upload(file_path, file_name='a file.txt')
    try:
        subfolder1 = root_folder.create_subfolder('copy_sub')
        try:
            a_file.copy(subfolder1)
            print(subfolder1.get_items(limit=10, offset=0))
            subfolder2 = root_folder.create_subfolder('copy_sub2')
            try:
                subfolder1.copy(subfolder2)
                print(subfolder2.get_items(limit=10, offset=0))
            finally:
                subfolder2.delete()
        finally:
            subfolder1.delete()
    finally:
        a_file.delete()


def move_item(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    a_file = root_folder.upload(file_path, file_name='a file.txt')
    try:
        subfolder1 = root_folder.create_subfolder('move_sub')
        try:
            a_file.move(subfolder1)
            print(subfolder1.get_items(limit=10, offset=0))
            subfolder2 = root_folder.create_subfolder('move_sub2')
            try:
                subfolder1.move(subfolder2)
                print(subfolder2.get_items(limit=10, offset=0))
            finally:
                subfolder2.delete()
        finally:
            try:
                subfolder1.delete()
            except BoxAPIException:
                pass
    finally:
        try:
            a_file.delete()
        except BoxAPIException:
            pass


def get_events(client):
    print(client.events().get_events(limit=100, stream_position='now'))


def get_latest_stream_position(client):
    print(client.events().get_latest_stream_position())


def long_poll(client):
    print(client.events().long_poll())


def _delete_leftover_group(existing_groups, group_name):
    """
    delete group if it already exists
    """
    existing_group = next((g for g in existing_groups if g.name == group_name), None)
    if existing_group:
        existing_group.delete()



def run_examples(oauth):

    client = Client(oauth)

    run_user_example(client)
    run_folder_examples(client)
    #run_collab_examples(client)
    rename_folder(client)
    get_folder_shared_link(client)
    upload_file(client)
    rename_file(client)
    update_file(client)
    search_files(client)
    copy_item(client)
    move_item(client)
    get_events(client)
    get_latest_stream_position(client)
    # long_poll(client)

    # Enterprise accounts only
    run_groups_example(client)
    run_metadata_example(client)



def main():

    # Please notice that you need to put in your client id and client secret in demo/auth.py in order to make this work.
    oauth, _, _ = authenticate()
    run_examples(oauth)
    os._exit(0)

if __name__ == '__main__':
    main()
