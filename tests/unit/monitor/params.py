
configurations = [
    {'id': 1, 'source': 'data_input', 'deliver_to':'data_processor', 'operation':'process_new_data', 'result': True},
    {'id': 2, 'source': 'data_processor', 'deliver_to':'data_output', 'operation':'process_new_events', 'result': True},
    {'id': 3, 'source': 'downloader', 'deliver_to':'manager', 'operation':'download_done', 'result': True},
    {'id': 4, 'source': 'manager', 'deliver_to':'downloader', 'operation':'download_file', 'result': True},
    {'id': 5, 'source': 'manager', 'deliver_to':'storage', 'operation':'commit_blob', 'result': True},
    {'id': 6, 'source': 'manager', 'deliver_to':'verifier', 'operation':'verification_requested', 'result': True},
    {'id': 7, 'source': 'verifier', 'deliver_to':'manager', 'operation':'handle_verification_result', 'result': True},
    {'id': 8, 'source': 'manager', 'deliver_to':'updater', 'operation':'proceed_with_update', 'result': True, 'verified': True},
    {'id': 9, 'source': 'storage', 'deliver_to':'manager', 'operation':'blob_committed', 'result': True},
    {'id': 10, 'source': 'storage', 'deliver_to':'verifier', 'operation':'blob_committed', 'result': True},
    {'id': 11, 'source': 'verifier', 'deliver_to':'storage', 'operation':'get_blob', 'result': True},
    {'id': 12, 'source': 'verifier', 'deliver_to':'storage', 'operation':'commit_sealed_blob', 'result': True, 'verified': True},
    {'id': 13, 'source': 'storage', 'deliver_to':'verifier', 'operation':'blob_content', 'result': True},
    {'id': 14, 'source': 'updater', 'deliver_to':'storage', 'operation':'get_blob', 'result': True},
    {'id': 15, 'source': 'data_processor', 'deliver_to':'data_input', 'operation':'check_data', 'result': False},
    {'id': 16, 'source': 'data_output', 'deliver_to':'data_input', 'operation':'check_data', 'result': False},
    {'id': 17, 'source': 'manager', 'deliver_to':'data_input', 'operation':'check_data', 'result': False}
]
