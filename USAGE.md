# Usage
**Examples**
- [Backup](#backup)
  - [Backup with an Integrity Check](#backup-with-an-integrity-check)
- [Restore](#restore)
  - [Restore with an Integrity Check](#restore-with-an-integrity-check)

## Backup
A simple run that backs up a database:

```bash
mvn compile exec:java \
  -Dexec.mainClass=com.google.cloud.pontem.CloudSpannerDatabaseBackup \
  -Dexec.args="--runner=DataflowRunner \
               --project=my-cloud-spanner-project \
               --gcpTempLocation=gs://my-cloud-spanner-project/tmp \
               --inputSpannerInstanceId=my-cloud-spanner-project-db \
               --inputSpannerDatabaseId=words2 \
               --outputFolder=gs://my-cloud-spanner-project/backups/latest \
               --projectId=my-cloud-spanner-project" \
  -Pdataflow-runner
```

A sample run that queries and saves the table row counts while not saving table schemas:

```bash
mvn compile exec:java \
  -Dexec.mainClass=com.google.cloud.pontem.CloudSpannerDatabaseBackup \
  -Dexec.args="--runner=DataflowRunner \
               --project=my-cloud-spanner-project \
               --gcpTempLocation=gs://my-cloud-spanner-project/tmp \
               --inputSpannerInstanceId=my-cloud-spanner-project-db \
               --inputSpannerDatabaseId=words2 \
               --outputFolder=gs://my-cloud-spanner-project/backup_today \
               --projectId=my-cloud-spanner-project \
               --shouldQueryTableRowCounts=true \
               --shouldQueryTableSchema=false" \
  -Pdataflow-runner
```

### Backup with an Integrity Check
A simple sample run:

```bash
mvn compile exec:java \
     -Dexec.mainClass=com.google.cloud.pontem.CloudSpannerDatabaseBackupIntegrityCheck \
     -Dexec.args="--project=my-cloud-spanner-project \
                  --databaseBackupLocation=gs://my-cloud-spanner-project/multi-backup \
                  --job=2017-10-25_11_18_28-6233650047978038157"
```

A sample run that requires checking row counts against the meta-data file:

```bash
mvn compile exec:java \
     -Dexec.mainClass=com.google.cloud.pontem.CloudSpannerDatabaseBackupIntegrityCheck \
     -Dexec.args="--project=my-cloud-spanner-project \
                  --databaseBackupLocation=gs://my-cloud-spanner-project/multi-backup \
                  --job=2017-10-25_11_18_28-6233650047978038157 \
                  --checkRowCountsAgainstGcsMetadataFile=true"
```

## Restore
A simple restore of a database:

```bash
mvn compile exec:java \
  -Dexec.mainClass=com.google.cloud.pontem.CloudSpannerDatabaseRestore \
  -Dexec.args="--runner=DataflowRunner \
               --project=my-cloud-spanner-project \
               --gcpTempLocation=gs://my-cloud-spanner-project/tmp \
               --outputSpannerInstanceId=my-cloud-spanner-project-db \
               --outputSpannerDatabaseId=words2 \
               --inputFolder=gs://my-cloud-spanner-project/backups/latest \
               --projectId=my-cloud-spanner-project" \
  -Pdataflow-runner
```

A sample restore of a database with a smaller Spanner write batch size. Note
that you will need to get the number of mutations down to 20000 in order
to comply with [Spanner's limits](https://cloud.google.com/spanner/quotas):

```bash
mvn compile exec:java \
  -Dexec.mainClass=com.google.cloud.pontem.CloudSpannerDatabaseRestore \
  -Dexec.args="--runner=DataflowRunner \
               --project=my-cloud-spanner-project \
               --gcpTempLocation=gs://my-cloud-spanner-project/tmp \
               --outputSpannerInstanceId=my-cloud-spanner-project-db \
               --outputSpannerDatabaseId=words2 \
               --inputFolder=gs://my-cloud-spanner-project/today_backup \
               --projectId=my-cloud-spanner-project \
               --spannerWriteBatchSizeBytes=524288"
  -Pdataflow-runner
```

### Restore with an Integrity Check
A sample run:

```bash
mvn compile exec:java \
  -Dexec.mainClass=com.google.cloud.pontem.CloudSpannerDatabaseRestoreIntegrityCheck \
  -Dexec.args="--project=my-cloud-spanner-project \
               --backupJobId=2017-12-28_08_21_49-14004506096652894727 \
               --restoreJobId=2017-12-28_10_43_41-10818313728228686289 \
               --restoreJobId=2017-12-28_10_46_20-2492938473109299932 \
               --restoreJobId=2017-12-28_10_48_47-17657844663911609681 \
               --restoreJobId=2017-12-28_10_51_16-6862684906618456059 \
               --restoreJobId=2017-12-28_10_53_55-7680195084002915695 \
               --restoreJobId=2017-12-28_10_43_41-17045671774098975520 \
               --restoreJobId=2017-12-28_10_43_41-16236058809269230845 \
               --databaseBackupLocation=gs://my-cloud-spanner-project/words_db_apache2.2.0_b/ \
               --areAllTablesRestored=false"
```

A sample run that requires every table to have been restored:

```bash
mvn compile exec:java \
  -Dexec.mainClass=com.google.cloud.pontem.CloudSpannerDatabaseRestoreIntegrityCheck \
  -Dexec.args="--project=my-cloud-spanner-project \
               --backupJobId=2017-12-28_08_21_49-14004506096652894727 \
               --restoreJobId=2017-12-28_10_43_41-10818313728228686289 \
               --restoreJobId=2017-12-28_10_46_20-2492938473109299932 \
               --restoreJobId=2017-12-28_10_48_47-17657844663911609681 \
               --restoreJobId=2017-12-28_10_51_16-6862684906618456059 \
               --restoreJobId=2017-12-28_10_53_55-7680195084002915695 \
               --restoreJobId=2017-12-28_10_43_41-17045671774098975520 \
               --restoreJobId=2017-12-28_10_43_47-170458491231849489454 \
               --restoreJobId=2017-12-28_10_43_41-16236058809269230845 \
               --databaseBackupLocation=gs://my-cloud-spanner-project/words_db_apache2.2.0_b/ \
               --areAllTablesRestored=true"
```