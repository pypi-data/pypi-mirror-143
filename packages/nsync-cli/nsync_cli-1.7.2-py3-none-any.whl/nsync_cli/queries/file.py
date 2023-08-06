save_version_outer = """
mutation {
  $batch
}
"""

save_version_inner = """
$qname: saveVersion(input: {
	key: $key
	path: $path
	uhash: $uhash
	permissions: $permissions
  timestamp: $timestamp
	fileType: $filetype
	ebody: $ebody
}) {
  transaction
  errors{
    messages
  }
}
"""

pull_versions = """
query{
  fileTransactions (first: 1, key: $key) {
    edges{
      node {
        id
        rawId
      }
    }
  }
  syncFiles(first:50, key: $key) {
    edges{
      node{
        path
        rawId
        latestVersion{
          rawId
          download
          permissions
          timestamp
          uhash
          isDir
          created
          transaction {
            id
            rawId
          }
        }
      }
    }
    pageInfo{
      startCursor
      endCursor
      hasNextPage
    }
  }
}
"""

pull_versions_page = """
query{
  syncFiles(first:50, key: $key, after: $after) {
    edges{
      node{
        path
        latestVersion{
          rawId
          download
          permissions
          timestamp
          uhash
          isDir
          created
          transaction {
            id
            rawId
          }
        }
      }
    }
    pageInfo{
      startCursor
      endCursor
      hasNextPage
    }
  }
}
"""

view_version = """
query {
  fileVersions(first: 1, id: $version_id) {
    edges{
      node{
        download
        rawId
        isDir
        linuxPerm
        timestamp
        syncFile{
          id
          path
        }
      }
    }
  }
}
"""

view_latest = """
query{
  syncFiles(first: 1, path: $path) {
    edges{
      node{
        path
        latestVersion{
          download
          rawId
          isDir
          linuxPerm
          timestamp
          syncFile{
            id
            path
          }
        }
      }
    }
  }
}
"""

version_by_transaction = """
query{
  fileVersions(
    first: 1
    transaction_Lte: $transaction
    syncFile_Path: $path
  ) {
    edges{
      node{
        rawId
        download
        isDir
        linuxPerm
        timestamp
        syncFile{
          id
          path
        }
      }
    }
  }
}
"""
