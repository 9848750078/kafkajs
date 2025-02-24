import boto3

# Initialize Lake Formation client
lakeformation = boto3.client('lakeformation')

def get_lf_tags(database_name, table_name, column_name):
    response = lakeformation.get_resource_lf_tags(
        Resource={
            'TableWithColumns': {
                'DatabaseName': database_name,
                'Name': table_name,
                'ColumnNames': [column_name]
            }
        }
    )
    return response['LFTagOnColumns']

def update_lf_tags(database_name, table_name, column_name, old_tag, new_tag):
    # Remove old LF-Tag
    lakeformation.remove_lf_tags_from_resource(
        Resource={
            'TableWithColumns': {
                'DatabaseName': database_name,
                'Name': table_name,
                'ColumnNames': [column_name]
            }
        },
        LFTags=[{'TagKey': 'Sensitivity', 'TagValues': [old_tag]}]
    )
    
    # Add new LF-Tag
    lakeformation.add_lf_tags_to_resource(
        Resource={
            'TableWithColumns': {
                'DatabaseName': database_name,
                'Name': table_name,
                'ColumnNames': [column_name]
            }
        },
        LFTags=[{'TagKey': 'Sensitivity', 'TagValues': [new_tag]}]
    )

def main():
    database_name = 'your_database'
    table_name = 'your_table'
    column_name = 'column1'
    old_tag = 'SPII'
    new_tag = 'NPII'
    
    current_tags = get_lf_tags(database_name, table_name, column_name)
    
    # Check if the old tag is present
    if any(tag['TagKey'] == 'Sensitivity' and old_tag in tag['TagValues'] for tag in current_tags):
        update_lf_tags(database_name, table_name, column_name, old_tag, new_tag)
        print(f"Updated LF-Tag for {column_name} from {old_tag} to {new_tag}")
    else:
        print(f"No update needed for {column_name}")

main()




-----------------------------------------------------------------------------------------------------------
error: Error Category: INVALID_ARGUMENT_ERROR; Failed Line Number: 59; KeyError: 'LFTagOnColumns'
