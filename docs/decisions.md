# Design decisions

## One file per snapshot instead of an appended CSV

Each collection run writes a new file (`snapshots/<date>/<timestamp>.csv`) on the
`data` branch instead of appending to a single growing CSV.

Reason: git stores a full version of a file on every commit that changes it. With
an accumulated CSV, each commit would add a complete copy of the file, so the
history of the `data` branch would grow to hundreds of MB per day (about 20 KB
per reading, 288 readings per day). With one file per reading, the history grows
by the same amount as the data itself. Power BI combines the files with the
Folder connector.
