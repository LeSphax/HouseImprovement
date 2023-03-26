from nilmtk2.dataset_converters.dataport.download_dataport import (
    download_dataport, 
    view_database_tables,
    view_buildings,
    view_data_window
)

    # see all available tables in the dataport database.
    view_database_tables(
        'username',
        'password',
        'database_schema'    # electricity 
    )

    # show the list of all available buildings
    view_buildings(
        'username',
        'password',
        'database_schema',  # electricity 
        'table_name'        # for example 'eg_realpower_1min', 'eg_current_15min'
    )

    # view data collection window of selected buildings
    view_data_window(
        'username',
        'password',
        'database_schema',  # electricity
        'table_name',       # for example 'eg_realpower_1min','eg_current_1hr'
        [18,26,43,44]       # data collection window of building 18,26,43 and 44 respectively
    )

    # download the dataset.
    For example, loading electricity_egauge_hours from 2018-11-17 to
    2019-12-17 of building 26
    download_dataport(
        'username',
        'password',
        '/path/output_filename.h5',
        'electricity',
        'eg_realpower_1hr',
        periods_to_load={ 26: ('2018-11-17', '2019-12-17')})