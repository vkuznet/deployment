#/usr/bin/env python
"""
WMAgent Configuration
"""

__revision__ = "$Id: WMAgentConfig.py,v 1.2 2010/01/26 22:03:40 mnorman Exp $"
__version__ = "$Revision: 1.2 $"

import os.path, socket
from WMCore.WMBase import getWMBASE
from WMCore.Configuration import Configuration
from WMAgentSecrets import databaseUrl

CONFIGDIR = os.path.normcase(os.path.abspath(__file__)).rsplit('/', 1)[0]
TOPDIR    = os.path.normpath(os.path.join(CONFIGDIR, '../../..'))
STATEDIR  = "%s/state/wmagent" % TOPDIR
LOGDIR    = "%s/logs/wmagent" % TOPDIR

# The following parameters may need to be changed.
serverHostName = socket.getfqdn().lower()
wmbsServicePort = 9999
workDirectory = STATEDIR
databaseSocket = "%s/state/mysql/mysql.sock" % TOPDIR

# The GroupUser and ConfigCache couch apps need to be installed into the
# configcache couch database. The JobDump couchapp needs to be installed
# into the jobdump database.  The GroupUser and ACDC couchapps needs to be
# install into the acdc database.
localCouchURL = "http://%s:5984" % serverHostName
centralCouchURL = "https://cmsweb.cern.ch/couchdb"
jobDumpDBName = "wmagent_jobdump"
jobSummaryDBName = "wmagent_summary"
acdcDBName = "wmagent_acdc"
workqueueDBName = 'workqueue'
workqueueInboxDbName = 'workqueue_inbox'
workloadSummaryDBName = "workloadsummary"
wmstatsDBName = "wmstats"

# Information for the workqueue, email of the administrator and the team names
# for this agent.
userEmail = "OP EMAIL"
agentTeams = "team1,team2,cmsdataops"
agentName = "WMAgentCommissioning"
agentNumber = 0

# List of BossAir plugins that this agent will use.
bossAirPlugins = ["CondorPlugin"]

# DBS Information.
localDBSUrl = "https://cmst0dbs.cern.ch:8443/cms_dbs_prod_tier0_writer/servlet/DBSServlet"
localDBSVersion = "DBS_2_0_8"
globalDBSUrl = "https://cmsdbsprod.cern.ch:8443/cms_dbs_prod_global_writer/servlet/DBSServlet"
globalDBSVersion = "DBS_2_0_8"
dbsMaxBlockSize = 5000000000000
dbsMaxBlockFiles = 500
dbsBlockTimeout = 86400

# Job retry information.  This includes the number of times a job will tried and
# how long it will sit in cool off.
maxJobRetries = 3
retryAlgoParams = {"create": 5000, "submit": 5000, "job": 5000}

# The amount of time to wait after a workflow has completed before archiving it.
workflowArchiveTimeout = 3600

# Global LogLevel
# For setting the general log level of the components
globalLogLevel = 'INFO'

#
# Nothing beyond this point should need to be changed.
#
config = Configuration()

config.section_("Agent")
config.Agent.hostName = serverHostName
config.Agent.contact = userEmail
config.Agent.teamName = agentTeams
config.Agent.agentName = agentName
config.Agent.agentNumber = agentNumber
config.Agent.useMsgService = False
config.Agent.useTrigger = False
config.Agent.useHeartbeat = True 

config.section_("General")
config.General.workDir = workDirectory

config.section_("JobStateMachine")
config.JobStateMachine.couchurl = localCouchURL
config.JobStateMachine.couchDBName = jobDumpDBName
config.JobStateMachine.jobSummaryDBName = jobSummaryDBName

config.section_("ACDC")
config.ACDC.couchurl = localCouchURL
config.ACDC.database = acdcDBName

config.section_("WorkloadSummary")
config.WorkloadSummary.couchurl = localCouchURL
config.WorkloadSummary.database = workloadSummaryDBName

config.section_("BossAir")
config.BossAir.pluginDir = "WMCore.BossAir.Plugins"
config.BossAir.pluginNames = bossAirPlugins
config.BossAir.nCondorProcesses = 1
config.BossAir.multicoreTaskTypes = ["MultiProcessing", "MultiProduction"]

config.section_("CoreDatabase")
config.CoreDatabase.connectUrl = databaseUrl
if databaseUrl.startswith("mysql"):
  config.CoreDatabase.socket = databaseSocket

config.section_("DashboardReporter")
config.DashboardReporter.dashboardHost = "cms-wmagent-job.cern.ch"
config.DashboardReporter.dashboardPort = 8884

config.component_('WorkQueueManager')
config.WorkQueueManager.namespace = "WMComponent.WorkQueueManager.WorkQueueManager"
config.WorkQueueManager.componentDir = config.General.workDir + "/WorkQueueManager"
config.WorkQueueManager.level = 'LocalQueue'
config.WorkQueueManager.logLevel = globalLogLevel
config.WorkQueueManager.couchurl = localCouchURL
config.WorkQueueManager.dbname = workqueueDBName
config.WorkQueueManager.inboxDatabase = workqueueInboxDbName
config.WorkQueueManager.queueParams = {}
config.WorkQueueManager.queueParams["ParentQueueCouchUrl"] = centralCouchURL + "/" + workqueueDBName

config.component_("DBSUpload")
config.DBSUpload.namespace = "WMComponent.DBSUpload.DBSUpload"
config.DBSUpload.componentDir = config.General.workDir + "/DBSUpload"
config.DBSUpload.logLevel = globalLogLevel
config.DBSUpload.workerThreads = 1
config.DBSUpload.pollInterval = 100

config.section_("DBSInterface")
#config.DBSInterface.DBSUrl = localDBSUrl
config.DBSInterface.DBSUrl = globalDBSUrl
config.DBSInterface.DBSVersion = localDBSVersion
config.DBSInterface.globalDBSUrl = globalDBSUrl
config.DBSInterface.globalDBSVersion = globalDBSVersion
config.DBSInterface.DBSBlockMaxSize = dbsMaxBlockSize
config.DBSInterface.DBSBlockMaxFiles = dbsMaxBlockFiles
config.DBSInterface.DBSBlockMaxTime = dbsBlockTimeout
config.DBSInterface.MaxFilesToCommit = 200
config.DBSInterface.doGlobalMigration = False

config.component_("PhEDExInjector")
config.PhEDExInjector.namespace = "WMComponent.PhEDExInjector.PhEDExInjector"
config.PhEDExInjector.componentDir = config.General.workDir + "/PhEDExInjector"
config.PhEDExInjector.logLevel = globalLogLevel
config.PhEDExInjector.maxThreads = 1
config.PhEDExInjector.subscribeMSS = True
config.PhEDExInjector.phedexurl = "https://cmsweb.cern.ch/phedex/datasvc/json/prod/"
config.PhEDExInjector.pollInterval = 100
config.PhEDExInjector.subscribeInterval = 43200

config.component_("JobAccountant")
config.JobAccountant.namespace = "WMComponent.JobAccountant.JobAccountant"
config.JobAccountant.componentDir = config.General.workDir + "/JobAccountant"
config.JobAccountant.logLevel = globalLogLevel
config.JobAccountant.workerThreads = 1
config.JobAccountant.pollInterval = 60

config.component_("JobCreator")
config.JobCreator.namespace = "WMComponent.JobCreator.JobCreator"
config.JobCreator.componentDir = config.General.workDir + "/JobCreator"
config.JobCreator.logLevel = globalLogLevel
config.JobCreator.maxThreads = 1
config.JobCreator.UpdateFromResourceControl = True
config.JobCreator.pollInterval = 120
# This is now OPTIONAL: It defaults to the componentDir
# However: In a production instance, this should be run on a high performance
# disk, and should probably NOT be run on the same disk as the JobArchiver
config.JobCreator.jobCacheDir = config.General.workDir + "/JobCreator/JobCache"
config.JobCreator.defaultJobType = "Processing"
config.JobCreator.workerThreads = 1

config.component_("JobSubmitter")
config.JobSubmitter.namespace = "WMComponent.JobSubmitter.JobSubmitter"
config.JobSubmitter.componentDir = config.General.workDir + "/JobSubmitter"
config.JobSubmitter.logLevel = globalLogLevel
config.JobSubmitter.maxThreads = 1
config.JobSubmitter.pollInterval = 120
config.JobSubmitter.workerThreads = 1
config.JobSubmitter.jobsPerWorker = 100
config.JobSubmitter.submitScript = os.path.join(os.environ["WMAGENT_ROOT"], "etc/submit.sh")

config.component_("JobTracker")
config.JobTracker.namespace = "WMComponent.JobTracker.JobTracker"
config.JobTracker.componentDir  = config.General.workDir + "/JobTracker"
config.JobTracker.logLevel = globalLogLevel
config.JobTracker.pollInterval = 60

config.component_("JobStatusLite")
config.JobStatusLite.namespace = "WMComponent.JobStatusLite.JobStatusLite"
config.JobStatusLite.componentDir  = config.General.workDir + "/JobStatusLite"
config.JobStatusLite.logLevel = globalLogLevel
config.JobStatusLite.pollInterval = 60
config.JobStatusLite.stateTimeouts = {"Error": 1800, "Running": 169200, "Pending": 360000}

config.component_("ErrorHandler")
config.ErrorHandler.namespace = "WMComponent.ErrorHandler.ErrorHandler"
config.ErrorHandler.componentDir  = config.General.workDir + "/ErrorHandler"
config.ErrorHandler.logLevel = globalLogLevel
config.ErrorHandler.maxRetries = maxJobRetries
config.ErrorHandler.pollInterval = 240

config.component_("RetryManager")
config.RetryManager.namespace = "WMComponent.RetryManager.RetryManager"
config.RetryManager.componentDir  = config.General.workDir + "/RetryManager"
config.RetryManager.logLevel = globalLogLevel
config.RetryManager.pollInterval = 240
config.RetryManager.plugins = {"default" : "SquaredAlgo"}
config.RetryManager.section_("SquaredAlgo")
config.RetryManager.SquaredAlgo.section_("default")
config.RetryManager.SquaredAlgo.default.coolOffTime = retryAlgoParams

config.component_("JobArchiver")
config.JobArchiver.namespace = "WMComponent.JobArchiver.JobArchiver"
config.JobArchiver.componentDir  = config.General.workDir + "/JobArchiver"
config.JobArchiver.pollInterval = 240
config.JobArchiver.logLevel = globalLogLevel
# This is now OPTIONAL, it defaults to the componentDir
# HOWEVER: Is is HIGHLY recommended that you do NOT run this on the same
# disk as the JobCreator
#config.JobArchiver.logDir = config.General.workDir + "/JobArchives"
config.JobArchiver.numberOfJobsToCluster = 1000

config.component_("TaskArchiver")
config.TaskArchiver.namespace = "WMComponent.TaskArchiver.TaskArchiver"
config.TaskArchiver.componentDir  = config.General.workDir + "/TaskArchiver"
config.TaskArchiver.logLevel = globalLogLevel
config.TaskArchiver.pollInterval = 240
config.TaskArchiver.timeOut      = workflowArchiveTimeout
config.TaskArchiver.useWorkQueue = True
config.TaskArchiver.workloadSummaryCouchURL = centralCouchURL
config.TaskArchiver.workloadSummaryCouchDBName = workloadSummaryDBName
config.TaskArchiver.histogramKeys = ["PeakValueRss", "PeakValueVsize", "TotalJobTime", "AvgEventTime"]
config.TaskArchiver.requireCouch  = True
config.TaskArchiver.uploadPublishInfo = False
config.TaskArchiver.uploadPublishDir  = None
config.TaskArchiver.userFileCacheURL = 'http://USERFILECACHEHOST:UFCPORT/userfilecache/'
# set to False couch data if request mgr is not used (Tier0, PromptSkiming)
config.TaskArchiver.useReqMgrForCompletionCheck = True
config.TaskArchiver.localCouchURL = "%s/%s" % (config.JobStateMachine.couchurl,  config.JobStateMachine.couchDBName)
config.TaskArchiver.localQueueURL = "%s/%s" % (config.WorkQueueManager.couchurl, config.WorkQueueManager.dbname)
config.TaskArchiver.localWMStatsURL = "%s/%s" % (config.JobStateMachine.couchurl, config.JobStateMachine.jobSummaryDBName)
config.TaskArchiver.centralWMStatsURL = centralCouchURL + "/" + wmstatsDBName
config.TaskArchiver.DataKeepDays = 1 # delete after a day maybe change to a week
config.TaskArchiver.cleanCouchInterval = 60 * 20 # 20 min

config.webapp_('WMBSService')
config.WMBSService.default_expires = 0
config.WMBSService.componentDir = os.path.join(config.General.workDir, "WMBSService")
config.WMBSService.Webtools.port = wmbsServicePort
config.WMBSService.Webtools.host = serverHostName
config.WMBSService.Webtools.environment = "devel"
config.WMBSService.templates = os.path.join(getWMBASE(), 'src/templates/WMCore/WebTools')
config.WMBSService.admin = config.Agent.contact
config.WMBSService.title = 'WMBS Data Service'
config.WMBSService.description = 'Provide WMBS related service call'

config.WMBSService.section_("security")
config.WMBSService.security.dangerously_insecure = True

config.WMBSService.section_('views')
active = config.WMBSService.views.section_('active')
wmbs = active.section_('wmbs')
wmbs.object = 'WMCore.WebTools.RESTApi'
wmbs.templates = os.path.join(getWMBASE(), 'src/templates/WMCore/WebTools/')
wmbs.section_('model')
wmbs.model.object = 'WMCore.HTTPFrontEnd.WMBS.WMBSRESTModel'
wmbs.section_('formatter')
wmbs.formatter.object = 'WMCore.WebTools.RESTFormatter'

wmbs.section_('couchConfig')
wmbs.couchConfig.couchURL = localCouchURL
wmbs.couchConfig.acdcDBName = acdcDBName
wmbs.couchConfig.jobDumpDBName = jobDumpDBName

wmagent = config.WMBSService.views.active.section_('wmagent')
wmagent.object = 'WMCore.WebTools.RESTApi'
wmagent.templates = os.path.join(os.environ["WMAGENT_ROOT"], 'data/templates/WMCore/WebTools/')
wmagent.section_('model')
wmagent.model.object = 'WMCore.HTTPFrontEnd.Agent.AgentRESTModel'
wmagent.section_('formatter')
wmagent.formatter.object = 'WMCore.WebTools.RESTFormatter'
wmagent.section_('couchConfig')
wmagent.couchConfig.couchURL = localCouchURL
wmagent.couchConfig.acdcDBName = acdcDBName
wmagent.couchConfig.jobDumpDBName = "wmagent_jobdump"

wmagentmonitor = config.WMBSService.views.active.section_('wmagentmonitor')
wmagentmonitor.object = 'WMCore.HTTPFrontEnd.Agent.AgentMonitorPage'
wmagentmonitor.templates = os.path.join(os.environ["WMAGENT_ROOT"], 'data/templates/WMCore/WebTools')
wmagentmonitor.javascript = os.path.join(os.environ["WMAGENT_ROOT"], 'data/javascript/')
wmagentmonitor.css = os.path.join(os.environ["WMAGENT_ROOT"], 'data/css/')
wmagentmonitor.html = os.path.join(os.environ["WMAGENT_ROOT"], 'data/html/')

wmbsmonitor = config.WMBSService.views.active.section_('wmbsmonitor')
wmbsmonitor.object = 'WMCore.HTTPFrontEnd.WMBS.WMBSMonitorPage'
wmbsmonitor.templates = os.path.join(os.environ["WMAGENT_ROOT"], 'data/templates/WMCore/WebTools')
wmbsmonitor.javascript = os.path.join(os.environ["WMAGENT_ROOT"], 'data/javascript/')
wmbsmonitor.css = os.path.join(os.environ["WMAGENT_ROOT"], 'data/css/')
wmbsmonitor.html = os.path.join(os.environ["WMAGENT_ROOT"], 'data/html/')



# Alert framework configuration

# common 'Alert' section (Alert "senders" use these values to determine destination)
config.section_("Alert")
# destination for the alert messages
config.Alert.address = "tcp://127.0.0.1:6557"
# control channel (internal alert system commands)
config.Alert.controlAddr = "tcp://127.0.0.1:6559"

# AlertProcessor component
# AlertProcessor values - values for Level soft, resp. critical
# are also needed by this AlertGenerator test
config.component_("AlertProcessor")
config.AlertProcessor.logLevel = "INFO"
config.AlertProcessor.namespace = "WMComponent.AlertProcessor.AlertProcessor"
config.AlertProcessor.componentDir = os.path.join(config.General.workDir, "AlertProcessor")
config.AlertProcessor.section_("critical")
config.AlertProcessor.section_("soft")
config.AlertProcessor.critical.level = 5
config.AlertProcessor.soft.level = 1
# where AlertProcessor is listening for incoming alert messages
config.AlertProcessor.address = config.Alert.address
config.AlertProcessor.controlAddr = config.Alert.controlAddr
config.AlertProcessor.soft.bufferSize = 3
# configure sinks associated with AlertProcessor
# there is one configured sink per soft, resp. critical alerts
# alerts don't get duplicated - i.e. either soft or critical alert is sent, not both
config.AlertProcessor.critical.section_("sinks")
config.AlertProcessor.soft.section_("sinks")
config.AlertProcessor.critical.sinks.section_("couch") # in tests used: ConfigSection("couch")
config.AlertProcessor.critical.sinks.couch.url = localCouchURL
config.AlertProcessor.critical.sinks.couch.database = "alerts_critical"
config.AlertProcessor.soft.sinks.section_("couch") # in tests used: ConfigSection("couch")
config.AlertProcessor.soft.sinks.couch.url = localCouchURL
config.AlertProcessor.soft.sinks.couch.database = "alerts_soft"
# alerts delivery via email
config.AlertProcessor.critical.sinks.section_("email")
# from must be a valid domain, at least when the destination address
# was @cern.ch: it said email is queued but was never delivered,
# may not always be the case though
# noreply@ will ensure that on an undeliverable email (e.g.
# for queueing too long to be delivered), the CERN exchange server
# generates a NDL (non-deliverable report) which again is
# undeliverable since the wmagent machine doesn't run any email service,
# with noreply@ it goes to /dev/null 
config.AlertProcessor.critical.sinks.email.fromAddr = "noreply@cern.ch"
config.AlertProcessor.critical.sinks.email.toAddr = ["wmagentalerts@gmail.com"] # add more in the list
config.AlertProcessor.critical.sinks.email.smtpServer = "cernmx.cern.ch"
config.AlertProcessor.critical.sinks.email.smtpUser = None
config.AlertProcessor.critical.sinks.email.smtpPass = None
config.AlertProcessor.soft.sinks.section_("email")
# from must be a valid domain, at least when the destination address
# was @cern.ch: it said email is queued but was never delivered,
# may not always be the case though
config.AlertProcessor.soft.sinks.email.fromAddr = "noreply@cern.ch"
config.AlertProcessor.soft.sinks.email.toAddr = ["wmagentalerts@gmail.com"] # add more in the list
config.AlertProcessor.soft.sinks.email.smtpServer = "cernmx.cern.ch"
config.AlertProcessor.soft.sinks.email.smtpUser = None
config.AlertProcessor.soft.sinks.email.smtpPass = None
config.AlertProcessor.critical.sinks.section_("file")
config.AlertProcessor.critical.sinks.file.outputfile = os.path.join(config.General.workDir, "AlertsFileSinkCritical.json")
config.AlertProcessor.soft.sinks.section_("file")
config.AlertProcessor.soft.sinks.file.outputfile = os.path.join(config.General.workDir, "AlertsFileSinkSoft.json")
# forward sink - should be remote addresses allowing alerts forwarding to a 
# different AlertProcessor, actually may not even be used ... disable this sink for now
#config.AlertProcessor.critical.sinks.section_("forward")
#config.AlertProcessor.critical.sinks.forward.address = "tcp://127.0.0.1:55555"
#config.AlertProcessor.critical.sinks.forward.controlAddr = "tcp://127.0.0.1:44444"
#config.AlertProcessor.critical.sinks.forward.label = "ForwardSink"
#config.AlertProcessor.soft.sinks.section_("forward")
#config.AlertProcessor.soft.sinks.forward.address = "tcp://127.0.0.1:55555"
#config.AlertProcessor.soft.sinks.forward.controlAddr = "tcp://127.0.0.1:44444"
#config.AlertProcessor.soft.sinks.forward.label = "ForwardSink"
# see comments on ticket 1640 - AlertCollector
# currently, for development & testing, CouchSink and AlertCollector are virtually the same thing
# though generally RESTSink is supposed to communicate with a generic REST server, not just CouchDB
config.AlertProcessor.critical.sinks.section_("rest")
config.AlertProcessor.critical.sinks.rest.uri = localCouchURL + "/" + "alertscollector"
# buffersize for the CMSCouch interface 
config.AlertProcessor.critical.sinks.rest.bufferSize = 10
config.AlertProcessor.soft.sinks.section_("rest")
config.AlertProcessor.soft.sinks.rest.uri = localCouchURL + "/" + "alertscollector"
# buffersize for the CMSCouch interface
config.AlertProcessor.critical.sinks.rest.bufferSize = 10

# AlertGenerator component
config.component_("AlertGenerator")
config.AlertGenerator.logLevel = "INFO"
config.AlertGenerator.namespace = "WMComponent.AlertGenerator.AlertGenerator"
config.AlertGenerator.componentDir = os.path.join(config.General.workDir, "AlertGenerator")
# configuration for overall machine load monitor: cpuPoller (percentage values)
config.AlertGenerator.section_("cpuPoller")
config.AlertGenerator.cpuPoller.soft = 8 # [percent]
config.AlertGenerator.cpuPoller.critical = 10 # [percent]
config.AlertGenerator.cpuPoller.pollInterval = 60 # [second]
# period during which measurements are collected before evaluating for possible alert triggering 
config.AlertGenerator.cpuPoller.period = 300 # [second]
# configuration for overall used physical memory monitor: memPoller (percentage of total physical memory)
config.AlertGenerator.section_("memPoller")
config.AlertGenerator.memPoller.soft = 85 # [percent]
config.AlertGenerator.memPoller.critical = 90 # [percent]
config.AlertGenerator.memPoller.pollInterval = 60 # [second]
# period during which measurements are collected before evaluating for possible alert triggering
config.AlertGenerator.memPoller.period = 300 # [second]
# configuration for available disk space monitor: diskSpacePoller (percentage usage per partition)
config.AlertGenerator.section_("diskSpacePoller")
config.AlertGenerator.diskSpacePoller.soft = 70 # [percent]
config.AlertGenerator.diskSpacePoller.critical = 90 # [percent]
config.AlertGenerator.diskSpacePoller.pollInterval = 600 # [second]
# configuration for particular components CPU usage: componentCPUPoller (percentage values)
config.AlertGenerator.section_("componentsCPUPoller")
config.AlertGenerator.componentsCPUPoller.soft = 70 # [percent]
config.AlertGenerator.componentsCPUPoller.critical = 90 # [percent]
config.AlertGenerator.componentsCPUPoller.pollInterval = 60 # [second]
# period during which measurements are collected before evaluating for possible alert triggering
config.AlertGenerator.componentsCPUPoller.period = 300 # [second]
# configuration for particular components memory monitor: componentMemPoller (percentage of total physical memory)
config.AlertGenerator.section_("componentsMemPoller")
config.AlertGenerator.componentsMemPoller.soft = 3 # [percent]
config.AlertGenerator.componentsMemPoller.critical = 5 # [percent] 
config.AlertGenerator.componentsMemPoller.pollInterval = 60  # [second]
# period during which measurements are collected before evaluating for possible alert triggering
config.AlertGenerator.componentsMemPoller.period = 300 # [second]
# configuration for CouchDB database size monitor: couchDbSizePoller (gigabytes values)
config.AlertGenerator.section_("couchDbSizePoller")
config.AlertGenerator.couchDbSizePoller.couchURL = localCouchURL
config.AlertGenerator.couchDbSizePoller.soft = 600 # GB
config.AlertGenerator.couchDbSizePoller.critical = 650 # GB
config.AlertGenerator.couchDbSizePoller.pollInterval = 600 # [second]
# configuration for CouchDB CPU monitor: couchCPUPoller (percentage values)
config.AlertGenerator.section_("couchCPUPoller")
config.AlertGenerator.couchCPUPoller.couchURL = localCouchURL
config.AlertGenerator.couchCPUPoller.soft = 250 # [percent]
config.AlertGenerator.couchCPUPoller.critical = 300 # [percent]
config.AlertGenerator.couchCPUPoller.pollInterval = 60 # [second]
# period during which measurements are collected before evaluating for possible alert triggering
config.AlertGenerator.couchCPUPoller.period = 300 # [second]
# configuration for CouchDB memory monitor: couchMemPoller (percentage values)
config.AlertGenerator.section_("couchMemPoller")
config.AlertGenerator.couchMemPoller.couchURL = localCouchURL
config.AlertGenerator.couchMemPoller.soft = 7 # [percent]
config.AlertGenerator.couchMemPoller.critical = 10 # [percent]
config.AlertGenerator.couchMemPoller.pollInterval = 60 # [second]
# period during which measurements are collected before evaluating for possible alert triggering
config.AlertGenerator.couchMemPoller.period = 300 # [second]
# configuration for CouchDB HTTP errors poller: couchErrorsPoller (number of error occurrences)
# (once certain threshold of the HTTP error counters is exceeded, poller keeps sending alerts)
config.AlertGenerator.section_("couchErrorsPoller")
config.AlertGenerator.couchErrorsPoller.couchURL = localCouchURL
config.AlertGenerator.couchErrorsPoller.soft = 100 # [number of error occurrences]
config.AlertGenerator.couchErrorsPoller.critical = 200 # [number of error occurrences]
# remove 404 for the moment, there is way too many of them and no interest generated
config.AlertGenerator.couchErrorsPoller.observables = (403, 500) # HTTP status codes to watch over
config.AlertGenerator.couchErrorsPoller.pollInterval = 600 # [second]

# mysql*Poller sections were made optional and are defined in the
# wmagent-mod-config file
# configuration for MySQL server CPU monitor: mysqlCPUPoller (percentage values)
if databaseUrl.startswith("mysql"):
  config.AlertGenerator.section_("mysqlCPUPoller")
  config.AlertGenerator.mysqlCPUPoller.soft = 200 # [percent]
  config.AlertGenerator.mysqlCPUPoller.critical = 250 # [percent]
  config.AlertGenerator.mysqlCPUPoller.pollInterval = 60 # [second]
  # period during which measurements are collected before evaluating for possible alert triggering
  config.AlertGenerator.mysqlCPUPoller.period = 300 # [second]
  # configuration for MySQL memory monitor: mysqlMemPoller (percentage values)
  config.AlertGenerator.section_("mysqlMemPoller")
  config.AlertGenerator.mysqlMemPoller.soft = 20 # [percent]
  config.AlertGenerator.mysqlMemPoller.critical = 25 # [percent]
  config.AlertGenerator.mysqlMemPoller.pollInterval = 60 # [second]
  # period during which measurements are collected before evaluating for possible alert triggering
  config.AlertGenerator.mysqlMemPoller.period = 300 # [second]
  # configuration for MySQL database size: mysqlDbSizePoller (gigabytes values)
  config.AlertGenerator.section_("mysqlDbSizePoller")
  config.AlertGenerator.mysqlDbSizePoller.soft = 20 # GB
  config.AlertGenerator.mysqlDbSizePoller.critical = 25 # GB
  config.AlertGenerator.mysqlDbSizePoller.pollInterval = 600 # [second]

# alerts-related stuff associated with components, these values shall later
# be moved into respective configuration sections 
# e.g. next item(s) will be from WorkQueueManager when a special necessary view is implemented
config.DBSUpload.alertUploadQueueSize = 2000

config.component_("AnalyticsDataCollector")
config.AnalyticsDataCollector.namespace = "WMComponent.AnalyticsDataCollector.AnalyticsDataCollector"
config.AnalyticsDataCollector.componentDir  = config.General.workDir + "/AnalyticsDataCollector"
config.AnalyticsDataCollector.logLevel = globalLogLevel
config.AnalyticsDataCollector.pollInterval = 600
config.AnalyticsDataCollector.localCouchURL = "%s/%s" % (config.JobStateMachine.couchurl,  config.JobStateMachine.couchDBName)
config.AnalyticsDataCollector.localQueueURL = "%s/%s" % (config.WorkQueueManager.couchurl, config.WorkQueueManager.dbname)
config.AnalyticsDataCollector.localWMStatsURL = "%s/%s" % (config.JobStateMachine.couchurl, config.JobStateMachine.jobSummaryDBName)
config.AnalyticsDataCollector.centralWMStatsURL = centralCouchURL + "/" + wmstatsDBName 
config.AnalyticsDataCollector.summaryLevel = "task"
