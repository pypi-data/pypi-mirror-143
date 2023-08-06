# target-airtable

![Release-Publish](https://github.com/ednarb29/target-airtable/actions/workflows/automatic-releases.yml/badge.svg)

This is a [Singer](https://singer.io) target that reads JSON-formatted data from stdin
following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md) and
persists it to [Airtable](https://airtable.com/).

## Install

Implemented and tested with Python 3.9.0. It is recommented to install this target into a
separate virtual environment to avoid dependency conflicts. Clone the repository and install
it from source:

```bash
› pip install target-airtable
```

## Use

target-airtable takes two types of input:

1. A config file containing
   - **api_token** (from your Airtable account)
   - **base** (the Airtable base id)
   - **endpoint** (optional, default="https://api.airtable.com/v0", the Airtable API endpoint)
   - **typecast** (optional, default=True, tries to cast types according to your Airtable table schema)
   - **output_schema** (optional, default=False, collects and write the (flattened) stream schema to a file)
   - **output_schema_path** (optional, default="", the output path to write the schema file)
   - **failed_insert_exception** (optional, default=True, raises an exception for any failed insert instead of error
     only)
   - **upsert** (optional, default=False, if set to True, it updates existing records and inserts new ones from the
     received streams. The parameter unique_field_name might be specified. Exceptions will be thrown if duplicate records
     are found both in the data to be upserted and the existing table data)
   - **unique_field_name** (optional, default="id", the field name which is assumed to be unique)
2. A stream of Singer-formatted data on stdin

target-airtable replicates the incomming streams from a tap into Airtable tables with the same name as the
stream. Make sure that these tables and the fields exist in your selected Airtable base.

If you want to make sure how the (flattened) schema has to look like in Airtable, set the option `output_schema` to
True. A file with the required table fields will be written to `output_schema_path/output_schema.txt` and no
records will be submitted to Airtable.


Create a config file with your configuration data:

```json
{
  "api_token": "my_token",
  "base": "my_base",
  "endpoint": "https://api.airtable.com/v0",
  "typecast": true,
  "output_schema": false,
  "output_schema_path": "",
  "failed_insert_exception": true,
  "upsert": false,
  "unique_field_name": "id"
}
```
```bash
› tap-some-api | target-airtable --config config.json
```

where `tap-some-api` is a [Singer Tap](https://singer.io).

# Want to help?
Fork, improve and PR.
