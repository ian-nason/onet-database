args <- commandArgs(TRUE)
flavor <- if(length(args)>=3) args[[3]] else 'patched'
.libPaths(c(file.path(args[[4]],flavor),.libPaths()))
library(datapond)
cat('R',R.version.string,'duckdb',as.character(packageVersion('duckdb')),'datapond',as.character(packageVersion('datapond')),'\n')
cfg <- list(memory_limit='128MiB',threads='1',max_temp_directory_size='0B',autoinstall_known_extensions='false')
options(datapond.registry_url=args[[1]],datapond.cache_dir=args[[2]],datapond.duckdb_config=cfg)
driver <- duckdb::duckdb(config=cfg)
probe <- DBI::dbConnect(driver)
stopifnot(isTRUE(DBI::dbGetQuery(probe,"SELECT installed FROM duckdb_extensions() WHERE extension_name='httpfs'")$installed[[1]]))
DBI::dbDisconnect(probe,shutdown=TRUE)
if(flavor=='cran') {
  originalDuckdb <- duckdb::duckdb
  testthat::local_mocked_bindings(duckdb=function(...) originalDuckdb(...,config=cfg),.package='duckdb')
  cat('CRAN driver constructor bounded by test harness; datapond functions unchanged.\n')
}
# dp_connect calls INSTALL; replace only that instruction in this process with
# LOAD of the preinstalled extension. No software download/install is allowed.
originalExecute <- DBI::dbExecute
testthat::local_mocked_bindings(dbExecute=function(conn,statement,...) {
  if(grepl('INSTALL httpfs',statement,fixed=TRUE)) statement <- gsub('INSTALL httpfs','LOAD httpfs',statement,fixed=TRUE)
  originalExecute(conn,statement,...)
},.package='DBI')
con <- dp_connect('onet',quiet=TRUE)
tryCatch({
  stopifnot(DBI::dbGetQuery(con,'SELECT count(*) AS n FROM occupation_data')$n[[1]]==1016)
  stopifnot(DBI::dbGetQuery(con,'SELECT sum(row_count) AS n FROM _metadata')$n[[1]]==468857)
  stopifnot(nrow(dp_describe(con))==12,nrow(dp_describe(con,table='work_context'))==16)
  stopifnot(DBI::dbGetQuery(con,'SELECT count(*) AS n FROM _columns')$n[[1]]==89)
  x <- DBI::dbGetQuery(con,"SELECT title,data_value,standard_error FROM work_context WHERE onet_soc_code='11-1011.00' AND element_id='4.C.1.a.2.c' AND scale_id='CX' AND category IS NULL")
  stopifnot(nrow(x)==1,abs(x$data_value[[1]]-3.07)<1e-10,abs(x$standard_error[[1]]-0.2851)<1e-10)
  print(x)
  print(dplyr::collect(utils::head(dplyr::tbl(con,'v_work_context_means'),3)))
  cat('R immutable public HTTPS consumer PASS\n')
},finally=dp_disconnect(con))
