# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'ApplicationAlarmMetricArgs',
    'ApplicationAlarmArgs',
    'ApplicationComponentConfigurationArgs',
    'ApplicationComponentMonitoringSettingArgs',
    'ApplicationConfigurationDetailsArgs',
    'ApplicationCustomComponentArgs',
    'ApplicationHAClusterPrometheusExporterArgs',
    'ApplicationHANAPrometheusExporterArgs',
    'ApplicationJMXPrometheusExporterArgs',
    'ApplicationLogPatternSetArgs',
    'ApplicationLogPatternArgs',
    'ApplicationLogArgs',
    'ApplicationSubComponentConfigurationDetailsArgs',
    'ApplicationSubComponentTypeConfigurationArgs',
    'ApplicationTagArgs',
    'ApplicationWindowsEventArgs',
]

@pulumi.input_type
class ApplicationAlarmMetricArgs:
    def __init__(__self__, *,
                 alarm_metric_name: pulumi.Input[str]):
        """
        A metric to be monitored for the component.
        :param pulumi.Input[str] alarm_metric_name: The name of the metric to be monitored for the component.
        """
        pulumi.set(__self__, "alarm_metric_name", alarm_metric_name)

    @property
    @pulumi.getter(name="alarmMetricName")
    def alarm_metric_name(self) -> pulumi.Input[str]:
        """
        The name of the metric to be monitored for the component.
        """
        return pulumi.get(self, "alarm_metric_name")

    @alarm_metric_name.setter
    def alarm_metric_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "alarm_metric_name", value)


@pulumi.input_type
class ApplicationAlarmArgs:
    def __init__(__self__, *,
                 alarm_name: pulumi.Input[str],
                 severity: Optional[pulumi.Input['ApplicationAlarmSeverity']] = None):
        """
        A CloudWatch alarm to be monitored for the component.
        :param pulumi.Input[str] alarm_name: The name of the CloudWatch alarm to be monitored for the component.
        :param pulumi.Input['ApplicationAlarmSeverity'] severity: Indicates the degree of outage when the alarm goes off.
        """
        pulumi.set(__self__, "alarm_name", alarm_name)
        if severity is not None:
            pulumi.set(__self__, "severity", severity)

    @property
    @pulumi.getter(name="alarmName")
    def alarm_name(self) -> pulumi.Input[str]:
        """
        The name of the CloudWatch alarm to be monitored for the component.
        """
        return pulumi.get(self, "alarm_name")

    @alarm_name.setter
    def alarm_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "alarm_name", value)

    @property
    @pulumi.getter
    def severity(self) -> Optional[pulumi.Input['ApplicationAlarmSeverity']]:
        """
        Indicates the degree of outage when the alarm goes off.
        """
        return pulumi.get(self, "severity")

    @severity.setter
    def severity(self, value: Optional[pulumi.Input['ApplicationAlarmSeverity']]):
        pulumi.set(self, "severity", value)


@pulumi.input_type
class ApplicationComponentConfigurationArgs:
    def __init__(__self__, *,
                 configuration_details: Optional[pulumi.Input['ApplicationConfigurationDetailsArgs']] = None,
                 sub_component_type_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationSubComponentTypeConfigurationArgs']]]] = None):
        """
        The configuration settings of the component.
        :param pulumi.Input['ApplicationConfigurationDetailsArgs'] configuration_details: The configuration settings
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationSubComponentTypeConfigurationArgs']]] sub_component_type_configurations: Sub component configurations of the component.
        """
        if configuration_details is not None:
            pulumi.set(__self__, "configuration_details", configuration_details)
        if sub_component_type_configurations is not None:
            pulumi.set(__self__, "sub_component_type_configurations", sub_component_type_configurations)

    @property
    @pulumi.getter(name="configurationDetails")
    def configuration_details(self) -> Optional[pulumi.Input['ApplicationConfigurationDetailsArgs']]:
        """
        The configuration settings
        """
        return pulumi.get(self, "configuration_details")

    @configuration_details.setter
    def configuration_details(self, value: Optional[pulumi.Input['ApplicationConfigurationDetailsArgs']]):
        pulumi.set(self, "configuration_details", value)

    @property
    @pulumi.getter(name="subComponentTypeConfigurations")
    def sub_component_type_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationSubComponentTypeConfigurationArgs']]]]:
        """
        Sub component configurations of the component.
        """
        return pulumi.get(self, "sub_component_type_configurations")

    @sub_component_type_configurations.setter
    def sub_component_type_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationSubComponentTypeConfigurationArgs']]]]):
        pulumi.set(self, "sub_component_type_configurations", value)


@pulumi.input_type
class ApplicationComponentMonitoringSettingArgs:
    def __init__(__self__, *,
                 component_configuration_mode: pulumi.Input['ApplicationComponentMonitoringSettingComponentConfigurationMode'],
                 tier: pulumi.Input[str],
                 component_arn: Optional[pulumi.Input[str]] = None,
                 component_name: Optional[pulumi.Input[str]] = None,
                 custom_component_configuration: Optional[pulumi.Input['ApplicationComponentConfigurationArgs']] = None,
                 default_overwrite_component_configuration: Optional[pulumi.Input['ApplicationComponentConfigurationArgs']] = None):
        """
        The monitoring setting of the component.
        :param pulumi.Input['ApplicationComponentMonitoringSettingComponentConfigurationMode'] component_configuration_mode: The component monitoring configuration mode.
        :param pulumi.Input[str] tier: The tier of the application component.
        :param pulumi.Input[str] component_arn: The ARN of the compnonent.
        :param pulumi.Input[str] component_name: The name of the component.
        :param pulumi.Input['ApplicationComponentConfigurationArgs'] custom_component_configuration: The monitoring configuration of the component.
        :param pulumi.Input['ApplicationComponentConfigurationArgs'] default_overwrite_component_configuration: The overwritten settings on default component monitoring configuration.
        """
        pulumi.set(__self__, "component_configuration_mode", component_configuration_mode)
        pulumi.set(__self__, "tier", tier)
        if component_arn is not None:
            pulumi.set(__self__, "component_arn", component_arn)
        if component_name is not None:
            pulumi.set(__self__, "component_name", component_name)
        if custom_component_configuration is not None:
            pulumi.set(__self__, "custom_component_configuration", custom_component_configuration)
        if default_overwrite_component_configuration is not None:
            pulumi.set(__self__, "default_overwrite_component_configuration", default_overwrite_component_configuration)

    @property
    @pulumi.getter(name="componentConfigurationMode")
    def component_configuration_mode(self) -> pulumi.Input['ApplicationComponentMonitoringSettingComponentConfigurationMode']:
        """
        The component monitoring configuration mode.
        """
        return pulumi.get(self, "component_configuration_mode")

    @component_configuration_mode.setter
    def component_configuration_mode(self, value: pulumi.Input['ApplicationComponentMonitoringSettingComponentConfigurationMode']):
        pulumi.set(self, "component_configuration_mode", value)

    @property
    @pulumi.getter
    def tier(self) -> pulumi.Input[str]:
        """
        The tier of the application component.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: pulumi.Input[str]):
        pulumi.set(self, "tier", value)

    @property
    @pulumi.getter(name="componentARN")
    def component_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the compnonent.
        """
        return pulumi.get(self, "component_arn")

    @component_arn.setter
    def component_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "component_arn", value)

    @property
    @pulumi.getter(name="componentName")
    def component_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the component.
        """
        return pulumi.get(self, "component_name")

    @component_name.setter
    def component_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "component_name", value)

    @property
    @pulumi.getter(name="customComponentConfiguration")
    def custom_component_configuration(self) -> Optional[pulumi.Input['ApplicationComponentConfigurationArgs']]:
        """
        The monitoring configuration of the component.
        """
        return pulumi.get(self, "custom_component_configuration")

    @custom_component_configuration.setter
    def custom_component_configuration(self, value: Optional[pulumi.Input['ApplicationComponentConfigurationArgs']]):
        pulumi.set(self, "custom_component_configuration", value)

    @property
    @pulumi.getter(name="defaultOverwriteComponentConfiguration")
    def default_overwrite_component_configuration(self) -> Optional[pulumi.Input['ApplicationComponentConfigurationArgs']]:
        """
        The overwritten settings on default component monitoring configuration.
        """
        return pulumi.get(self, "default_overwrite_component_configuration")

    @default_overwrite_component_configuration.setter
    def default_overwrite_component_configuration(self, value: Optional[pulumi.Input['ApplicationComponentConfigurationArgs']]):
        pulumi.set(self, "default_overwrite_component_configuration", value)


@pulumi.input_type
class ApplicationConfigurationDetailsArgs:
    def __init__(__self__, *,
                 alarm_metrics: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationAlarmMetricArgs']]]] = None,
                 alarms: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationAlarmArgs']]]] = None,
                 h_a_cluster_prometheus_exporter: Optional[pulumi.Input['ApplicationHAClusterPrometheusExporterArgs']] = None,
                 h_ana_prometheus_exporter: Optional[pulumi.Input['ApplicationHANAPrometheusExporterArgs']] = None,
                 j_mx_prometheus_exporter: Optional[pulumi.Input['ApplicationJMXPrometheusExporterArgs']] = None,
                 logs: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationLogArgs']]]] = None,
                 windows_events: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationWindowsEventArgs']]]] = None):
        """
        The configuration settings.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationAlarmMetricArgs']]] alarm_metrics: A list of metrics to monitor for the component.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationAlarmArgs']]] alarms: A list of alarms to monitor for the component.
        :param pulumi.Input['ApplicationHAClusterPrometheusExporterArgs'] h_a_cluster_prometheus_exporter: The HA cluster Prometheus Exporter settings.
        :param pulumi.Input['ApplicationHANAPrometheusExporterArgs'] h_ana_prometheus_exporter: The HANA DB Prometheus Exporter settings.
        :param pulumi.Input['ApplicationJMXPrometheusExporterArgs'] j_mx_prometheus_exporter: The JMX Prometheus Exporter settings.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationLogArgs']]] logs: A list of logs to monitor for the component.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationWindowsEventArgs']]] windows_events: A list of Windows Events to log.
        """
        if alarm_metrics is not None:
            pulumi.set(__self__, "alarm_metrics", alarm_metrics)
        if alarms is not None:
            pulumi.set(__self__, "alarms", alarms)
        if h_a_cluster_prometheus_exporter is not None:
            pulumi.set(__self__, "h_a_cluster_prometheus_exporter", h_a_cluster_prometheus_exporter)
        if h_ana_prometheus_exporter is not None:
            pulumi.set(__self__, "h_ana_prometheus_exporter", h_ana_prometheus_exporter)
        if j_mx_prometheus_exporter is not None:
            pulumi.set(__self__, "j_mx_prometheus_exporter", j_mx_prometheus_exporter)
        if logs is not None:
            pulumi.set(__self__, "logs", logs)
        if windows_events is not None:
            pulumi.set(__self__, "windows_events", windows_events)

    @property
    @pulumi.getter(name="alarmMetrics")
    def alarm_metrics(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationAlarmMetricArgs']]]]:
        """
        A list of metrics to monitor for the component.
        """
        return pulumi.get(self, "alarm_metrics")

    @alarm_metrics.setter
    def alarm_metrics(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationAlarmMetricArgs']]]]):
        pulumi.set(self, "alarm_metrics", value)

    @property
    @pulumi.getter
    def alarms(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationAlarmArgs']]]]:
        """
        A list of alarms to monitor for the component.
        """
        return pulumi.get(self, "alarms")

    @alarms.setter
    def alarms(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationAlarmArgs']]]]):
        pulumi.set(self, "alarms", value)

    @property
    @pulumi.getter(name="hAClusterPrometheusExporter")
    def h_a_cluster_prometheus_exporter(self) -> Optional[pulumi.Input['ApplicationHAClusterPrometheusExporterArgs']]:
        """
        The HA cluster Prometheus Exporter settings.
        """
        return pulumi.get(self, "h_a_cluster_prometheus_exporter")

    @h_a_cluster_prometheus_exporter.setter
    def h_a_cluster_prometheus_exporter(self, value: Optional[pulumi.Input['ApplicationHAClusterPrometheusExporterArgs']]):
        pulumi.set(self, "h_a_cluster_prometheus_exporter", value)

    @property
    @pulumi.getter(name="hANAPrometheusExporter")
    def h_ana_prometheus_exporter(self) -> Optional[pulumi.Input['ApplicationHANAPrometheusExporterArgs']]:
        """
        The HANA DB Prometheus Exporter settings.
        """
        return pulumi.get(self, "h_ana_prometheus_exporter")

    @h_ana_prometheus_exporter.setter
    def h_ana_prometheus_exporter(self, value: Optional[pulumi.Input['ApplicationHANAPrometheusExporterArgs']]):
        pulumi.set(self, "h_ana_prometheus_exporter", value)

    @property
    @pulumi.getter(name="jMXPrometheusExporter")
    def j_mx_prometheus_exporter(self) -> Optional[pulumi.Input['ApplicationJMXPrometheusExporterArgs']]:
        """
        The JMX Prometheus Exporter settings.
        """
        return pulumi.get(self, "j_mx_prometheus_exporter")

    @j_mx_prometheus_exporter.setter
    def j_mx_prometheus_exporter(self, value: Optional[pulumi.Input['ApplicationJMXPrometheusExporterArgs']]):
        pulumi.set(self, "j_mx_prometheus_exporter", value)

    @property
    @pulumi.getter
    def logs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationLogArgs']]]]:
        """
        A list of logs to monitor for the component.
        """
        return pulumi.get(self, "logs")

    @logs.setter
    def logs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationLogArgs']]]]):
        pulumi.set(self, "logs", value)

    @property
    @pulumi.getter(name="windowsEvents")
    def windows_events(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationWindowsEventArgs']]]]:
        """
        A list of Windows Events to log.
        """
        return pulumi.get(self, "windows_events")

    @windows_events.setter
    def windows_events(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationWindowsEventArgs']]]]):
        pulumi.set(self, "windows_events", value)


@pulumi.input_type
class ApplicationCustomComponentArgs:
    def __init__(__self__, *,
                 component_name: pulumi.Input[str],
                 resource_list: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        The custom grouped component.
        :param pulumi.Input[str] component_name: The name of the component.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resource_list: The list of resource ARNs that belong to the component.
        """
        pulumi.set(__self__, "component_name", component_name)
        pulumi.set(__self__, "resource_list", resource_list)

    @property
    @pulumi.getter(name="componentName")
    def component_name(self) -> pulumi.Input[str]:
        """
        The name of the component.
        """
        return pulumi.get(self, "component_name")

    @component_name.setter
    def component_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "component_name", value)

    @property
    @pulumi.getter(name="resourceList")
    def resource_list(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The list of resource ARNs that belong to the component.
        """
        return pulumi.get(self, "resource_list")

    @resource_list.setter
    def resource_list(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "resource_list", value)


@pulumi.input_type
class ApplicationHAClusterPrometheusExporterArgs:
    def __init__(__self__, *,
                 prometheus_port: Optional[pulumi.Input[str]] = None):
        """
        The HA cluster Prometheus Exporter settings.
        :param pulumi.Input[str] prometheus_port: Prometheus exporter port.
        """
        if prometheus_port is not None:
            pulumi.set(__self__, "prometheus_port", prometheus_port)

    @property
    @pulumi.getter(name="prometheusPort")
    def prometheus_port(self) -> Optional[pulumi.Input[str]]:
        """
        Prometheus exporter port.
        """
        return pulumi.get(self, "prometheus_port")

    @prometheus_port.setter
    def prometheus_port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "prometheus_port", value)


@pulumi.input_type
class ApplicationHANAPrometheusExporterArgs:
    def __init__(__self__, *,
                 agree_to_install_hanadb_client: pulumi.Input[bool],
                 h_ana_port: pulumi.Input[str],
                 h_anasid: pulumi.Input[str],
                 h_ana_secret_name: pulumi.Input[str],
                 prometheus_port: Optional[pulumi.Input[str]] = None):
        """
        The HANA DB Prometheus Exporter settings.
        :param pulumi.Input[bool] agree_to_install_hanadb_client: A flag which indicates agreeing to install SAP HANA DB client.
        :param pulumi.Input[str] h_ana_port: The HANA DB port.
        :param pulumi.Input[str] h_anasid: HANA DB SID.
        :param pulumi.Input[str] h_ana_secret_name: The secret name which manages the HANA DB credentials e.g. {
                 "username": "<>",
                 "password": "<>"
               }.
        :param pulumi.Input[str] prometheus_port: Prometheus exporter port.
        """
        pulumi.set(__self__, "agree_to_install_hanadb_client", agree_to_install_hanadb_client)
        pulumi.set(__self__, "h_ana_port", h_ana_port)
        pulumi.set(__self__, "h_anasid", h_anasid)
        pulumi.set(__self__, "h_ana_secret_name", h_ana_secret_name)
        if prometheus_port is not None:
            pulumi.set(__self__, "prometheus_port", prometheus_port)

    @property
    @pulumi.getter(name="agreeToInstallHANADBClient")
    def agree_to_install_hanadb_client(self) -> pulumi.Input[bool]:
        """
        A flag which indicates agreeing to install SAP HANA DB client.
        """
        return pulumi.get(self, "agree_to_install_hanadb_client")

    @agree_to_install_hanadb_client.setter
    def agree_to_install_hanadb_client(self, value: pulumi.Input[bool]):
        pulumi.set(self, "agree_to_install_hanadb_client", value)

    @property
    @pulumi.getter(name="hANAPort")
    def h_ana_port(self) -> pulumi.Input[str]:
        """
        The HANA DB port.
        """
        return pulumi.get(self, "h_ana_port")

    @h_ana_port.setter
    def h_ana_port(self, value: pulumi.Input[str]):
        pulumi.set(self, "h_ana_port", value)

    @property
    @pulumi.getter(name="hANASID")
    def h_anasid(self) -> pulumi.Input[str]:
        """
        HANA DB SID.
        """
        return pulumi.get(self, "h_anasid")

    @h_anasid.setter
    def h_anasid(self, value: pulumi.Input[str]):
        pulumi.set(self, "h_anasid", value)

    @property
    @pulumi.getter(name="hANASecretName")
    def h_ana_secret_name(self) -> pulumi.Input[str]:
        """
        The secret name which manages the HANA DB credentials e.g. {
          "username": "<>",
          "password": "<>"
        }.
        """
        return pulumi.get(self, "h_ana_secret_name")

    @h_ana_secret_name.setter
    def h_ana_secret_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "h_ana_secret_name", value)

    @property
    @pulumi.getter(name="prometheusPort")
    def prometheus_port(self) -> Optional[pulumi.Input[str]]:
        """
        Prometheus exporter port.
        """
        return pulumi.get(self, "prometheus_port")

    @prometheus_port.setter
    def prometheus_port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "prometheus_port", value)


@pulumi.input_type
class ApplicationJMXPrometheusExporterArgs:
    def __init__(__self__, *,
                 host_port: Optional[pulumi.Input[str]] = None,
                 j_mxurl: Optional[pulumi.Input[str]] = None,
                 prometheus_port: Optional[pulumi.Input[str]] = None):
        """
        The JMX Prometheus Exporter settings.
        :param pulumi.Input[str] host_port: Java agent host port
        :param pulumi.Input[str] j_mxurl: JMX service URL.
        :param pulumi.Input[str] prometheus_port: Prometheus exporter port.
        """
        if host_port is not None:
            pulumi.set(__self__, "host_port", host_port)
        if j_mxurl is not None:
            pulumi.set(__self__, "j_mxurl", j_mxurl)
        if prometheus_port is not None:
            pulumi.set(__self__, "prometheus_port", prometheus_port)

    @property
    @pulumi.getter(name="hostPort")
    def host_port(self) -> Optional[pulumi.Input[str]]:
        """
        Java agent host port
        """
        return pulumi.get(self, "host_port")

    @host_port.setter
    def host_port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_port", value)

    @property
    @pulumi.getter(name="jMXURL")
    def j_mxurl(self) -> Optional[pulumi.Input[str]]:
        """
        JMX service URL.
        """
        return pulumi.get(self, "j_mxurl")

    @j_mxurl.setter
    def j_mxurl(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "j_mxurl", value)

    @property
    @pulumi.getter(name="prometheusPort")
    def prometheus_port(self) -> Optional[pulumi.Input[str]]:
        """
        Prometheus exporter port.
        """
        return pulumi.get(self, "prometheus_port")

    @prometheus_port.setter
    def prometheus_port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "prometheus_port", value)


@pulumi.input_type
class ApplicationLogPatternSetArgs:
    def __init__(__self__, *,
                 log_patterns: pulumi.Input[Sequence[pulumi.Input['ApplicationLogPatternArgs']]],
                 pattern_set_name: pulumi.Input[str]):
        """
        The log pattern set.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationLogPatternArgs']]] log_patterns: The log patterns of a set.
        :param pulumi.Input[str] pattern_set_name: The name of the log pattern set.
        """
        pulumi.set(__self__, "log_patterns", log_patterns)
        pulumi.set(__self__, "pattern_set_name", pattern_set_name)

    @property
    @pulumi.getter(name="logPatterns")
    def log_patterns(self) -> pulumi.Input[Sequence[pulumi.Input['ApplicationLogPatternArgs']]]:
        """
        The log patterns of a set.
        """
        return pulumi.get(self, "log_patterns")

    @log_patterns.setter
    def log_patterns(self, value: pulumi.Input[Sequence[pulumi.Input['ApplicationLogPatternArgs']]]):
        pulumi.set(self, "log_patterns", value)

    @property
    @pulumi.getter(name="patternSetName")
    def pattern_set_name(self) -> pulumi.Input[str]:
        """
        The name of the log pattern set.
        """
        return pulumi.get(self, "pattern_set_name")

    @pattern_set_name.setter
    def pattern_set_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "pattern_set_name", value)


@pulumi.input_type
class ApplicationLogPatternArgs:
    def __init__(__self__, *,
                 pattern: pulumi.Input[str],
                 pattern_name: pulumi.Input[str],
                 rank: pulumi.Input[int]):
        """
        The log pattern.
        :param pulumi.Input[str] pattern: The log pattern.
        :param pulumi.Input[str] pattern_name: The name of the log pattern.
        :param pulumi.Input[int] rank: Rank of the log pattern.
        """
        pulumi.set(__self__, "pattern", pattern)
        pulumi.set(__self__, "pattern_name", pattern_name)
        pulumi.set(__self__, "rank", rank)

    @property
    @pulumi.getter
    def pattern(self) -> pulumi.Input[str]:
        """
        The log pattern.
        """
        return pulumi.get(self, "pattern")

    @pattern.setter
    def pattern(self, value: pulumi.Input[str]):
        pulumi.set(self, "pattern", value)

    @property
    @pulumi.getter(name="patternName")
    def pattern_name(self) -> pulumi.Input[str]:
        """
        The name of the log pattern.
        """
        return pulumi.get(self, "pattern_name")

    @pattern_name.setter
    def pattern_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "pattern_name", value)

    @property
    @pulumi.getter
    def rank(self) -> pulumi.Input[int]:
        """
        Rank of the log pattern.
        """
        return pulumi.get(self, "rank")

    @rank.setter
    def rank(self, value: pulumi.Input[int]):
        pulumi.set(self, "rank", value)


@pulumi.input_type
class ApplicationLogArgs:
    def __init__(__self__, *,
                 log_type: pulumi.Input[str],
                 encoding: Optional[pulumi.Input['ApplicationLogEncoding']] = None,
                 log_group_name: Optional[pulumi.Input[str]] = None,
                 log_path: Optional[pulumi.Input[str]] = None,
                 pattern_set: Optional[pulumi.Input[str]] = None):
        """
        A log to be monitored for the component.
        :param pulumi.Input[str] log_type: The log type decides the log patterns against which Application Insights analyzes the log.
        :param pulumi.Input['ApplicationLogEncoding'] encoding: The type of encoding of the logs to be monitored.
        :param pulumi.Input[str] log_group_name: The CloudWatch log group name to be associated to the monitored log.
        :param pulumi.Input[str] log_path: The path of the logs to be monitored.
        :param pulumi.Input[str] pattern_set: The name of the log pattern set.
        """
        pulumi.set(__self__, "log_type", log_type)
        if encoding is not None:
            pulumi.set(__self__, "encoding", encoding)
        if log_group_name is not None:
            pulumi.set(__self__, "log_group_name", log_group_name)
        if log_path is not None:
            pulumi.set(__self__, "log_path", log_path)
        if pattern_set is not None:
            pulumi.set(__self__, "pattern_set", pattern_set)

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> pulumi.Input[str]:
        """
        The log type decides the log patterns against which Application Insights analyzes the log.
        """
        return pulumi.get(self, "log_type")

    @log_type.setter
    def log_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_type", value)

    @property
    @pulumi.getter
    def encoding(self) -> Optional[pulumi.Input['ApplicationLogEncoding']]:
        """
        The type of encoding of the logs to be monitored.
        """
        return pulumi.get(self, "encoding")

    @encoding.setter
    def encoding(self, value: Optional[pulumi.Input['ApplicationLogEncoding']]):
        pulumi.set(self, "encoding", value)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The CloudWatch log group name to be associated to the monitored log.
        """
        return pulumi.get(self, "log_group_name")

    @log_group_name.setter
    def log_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_group_name", value)

    @property
    @pulumi.getter(name="logPath")
    def log_path(self) -> Optional[pulumi.Input[str]]:
        """
        The path of the logs to be monitored.
        """
        return pulumi.get(self, "log_path")

    @log_path.setter
    def log_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_path", value)

    @property
    @pulumi.getter(name="patternSet")
    def pattern_set(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the log pattern set.
        """
        return pulumi.get(self, "pattern_set")

    @pattern_set.setter
    def pattern_set(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pattern_set", value)


@pulumi.input_type
class ApplicationSubComponentConfigurationDetailsArgs:
    def __init__(__self__, *,
                 alarm_metrics: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationAlarmMetricArgs']]]] = None,
                 logs: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationLogArgs']]]] = None,
                 windows_events: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationWindowsEventArgs']]]] = None):
        """
        The configuration settings of sub components.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationAlarmMetricArgs']]] alarm_metrics: A list of metrics to monitor for the component.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationLogArgs']]] logs: A list of logs to monitor for the component.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationWindowsEventArgs']]] windows_events: A list of Windows Events to log.
        """
        if alarm_metrics is not None:
            pulumi.set(__self__, "alarm_metrics", alarm_metrics)
        if logs is not None:
            pulumi.set(__self__, "logs", logs)
        if windows_events is not None:
            pulumi.set(__self__, "windows_events", windows_events)

    @property
    @pulumi.getter(name="alarmMetrics")
    def alarm_metrics(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationAlarmMetricArgs']]]]:
        """
        A list of metrics to monitor for the component.
        """
        return pulumi.get(self, "alarm_metrics")

    @alarm_metrics.setter
    def alarm_metrics(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationAlarmMetricArgs']]]]):
        pulumi.set(self, "alarm_metrics", value)

    @property
    @pulumi.getter
    def logs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationLogArgs']]]]:
        """
        A list of logs to monitor for the component.
        """
        return pulumi.get(self, "logs")

    @logs.setter
    def logs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationLogArgs']]]]):
        pulumi.set(self, "logs", value)

    @property
    @pulumi.getter(name="windowsEvents")
    def windows_events(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationWindowsEventArgs']]]]:
        """
        A list of Windows Events to log.
        """
        return pulumi.get(self, "windows_events")

    @windows_events.setter
    def windows_events(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationWindowsEventArgs']]]]):
        pulumi.set(self, "windows_events", value)


@pulumi.input_type
class ApplicationSubComponentTypeConfigurationArgs:
    def __init__(__self__, *,
                 sub_component_configuration_details: pulumi.Input['ApplicationSubComponentConfigurationDetailsArgs'],
                 sub_component_type: pulumi.Input['ApplicationSubComponentTypeConfigurationSubComponentType']):
        """
        One type sub component configurations for the component.
        :param pulumi.Input['ApplicationSubComponentConfigurationDetailsArgs'] sub_component_configuration_details: The configuration settings of sub components.
        :param pulumi.Input['ApplicationSubComponentTypeConfigurationSubComponentType'] sub_component_type: The sub component type.
        """
        pulumi.set(__self__, "sub_component_configuration_details", sub_component_configuration_details)
        pulumi.set(__self__, "sub_component_type", sub_component_type)

    @property
    @pulumi.getter(name="subComponentConfigurationDetails")
    def sub_component_configuration_details(self) -> pulumi.Input['ApplicationSubComponentConfigurationDetailsArgs']:
        """
        The configuration settings of sub components.
        """
        return pulumi.get(self, "sub_component_configuration_details")

    @sub_component_configuration_details.setter
    def sub_component_configuration_details(self, value: pulumi.Input['ApplicationSubComponentConfigurationDetailsArgs']):
        pulumi.set(self, "sub_component_configuration_details", value)

    @property
    @pulumi.getter(name="subComponentType")
    def sub_component_type(self) -> pulumi.Input['ApplicationSubComponentTypeConfigurationSubComponentType']:
        """
        The sub component type.
        """
        return pulumi.get(self, "sub_component_type")

    @sub_component_type.setter
    def sub_component_type(self, value: pulumi.Input['ApplicationSubComponentTypeConfigurationSubComponentType']):
        pulumi.set(self, "sub_component_type", value)


@pulumi.input_type
class ApplicationTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        A key-value pair to associate with a resource.
        :param pulumi.Input[str] key: The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        :param pulumi.Input[str] value: The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ApplicationWindowsEventArgs:
    def __init__(__self__, *,
                 event_levels: pulumi.Input[Sequence[pulumi.Input['ApplicationEventLevel']]],
                 event_name: pulumi.Input[str],
                 log_group_name: pulumi.Input[str],
                 pattern_set: Optional[pulumi.Input[str]] = None):
        """
        A Windows Event to be monitored for the component.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationEventLevel']]] event_levels: The levels of event to log. 
        :param pulumi.Input[str] event_name: The type of Windows Events to log.
        :param pulumi.Input[str] log_group_name: The CloudWatch log group name to be associated to the monitored log.
        :param pulumi.Input[str] pattern_set: The name of the log pattern set.
        """
        pulumi.set(__self__, "event_levels", event_levels)
        pulumi.set(__self__, "event_name", event_name)
        pulumi.set(__self__, "log_group_name", log_group_name)
        if pattern_set is not None:
            pulumi.set(__self__, "pattern_set", pattern_set)

    @property
    @pulumi.getter(name="eventLevels")
    def event_levels(self) -> pulumi.Input[Sequence[pulumi.Input['ApplicationEventLevel']]]:
        """
        The levels of event to log. 
        """
        return pulumi.get(self, "event_levels")

    @event_levels.setter
    def event_levels(self, value: pulumi.Input[Sequence[pulumi.Input['ApplicationEventLevel']]]):
        pulumi.set(self, "event_levels", value)

    @property
    @pulumi.getter(name="eventName")
    def event_name(self) -> pulumi.Input[str]:
        """
        The type of Windows Events to log.
        """
        return pulumi.get(self, "event_name")

    @event_name.setter
    def event_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "event_name", value)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> pulumi.Input[str]:
        """
        The CloudWatch log group name to be associated to the monitored log.
        """
        return pulumi.get(self, "log_group_name")

    @log_group_name.setter
    def log_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_group_name", value)

    @property
    @pulumi.getter(name="patternSet")
    def pattern_set(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the log pattern set.
        """
        return pulumi.get(self, "pattern_set")

    @pattern_set.setter
    def pattern_set(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pattern_set", value)


