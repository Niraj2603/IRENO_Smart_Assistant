import requests
from langchain.tools import Tool
from typing import Dict, Any
import json
import logging
from datetime import datetime, timedelta
from urllib.parse import quote

# Configure logging for IRENO tools
logger = logging.getLogger(__name__)

class IrenoAPITools:
    """IRENO API Tools for LangChain agent"""
    
    BASE_URL = "https://irenoakscluster.westus.cloudapp.azure.com/devicemgmt/v1/collector"
    KPI_BASE_URL = "https://irenoakscluster.westus.cloudapp.azure.com/kpimgmt/v1/kpi"
    
    def __init__(self):
        logger.info("🔧 Initializing IRENO API Tools")
        self.session = requests.Session()
        # Add any authentication headers if needed
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'IRENO-Smart-Assistant/1.0'
        })
        logger.info(f"🌐 Base URL: {self.BASE_URL}")
        logger.info(f"🌐 KPI URL: {self.KPI_BASE_URL}")
    
    def get_offline_collectors(self, query: str = "") -> str:
        """
        Fetch information about offline collectors from IRENO API.
        Use this when users ask about offline collectors, down devices, or disconnected equipment.
        """
        logger.info(f"📡 API Call: get_offline_collectors - Query: '{query}'")
        try:
            url = f"{self.BASE_URL}?status=offline"
            logger.info(f"🌐 Making request to: {url}")
            
            response = self.session.get(url, timeout=15)  # Increased timeout
            logger.info(f"📊 Response status: {response.status_code}")
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"📦 Received data type: {type(data)}, Size: {len(str(data))} chars")
            
            # Format the response for the AI
            if isinstance(data, dict) and 'collectors' in data:
                collectors_list = data['collectors']
                count = data.get('totalCount', len(collectors_list))
                
                if count == 0:
                    return "Good news! All collectors are currently online. No offline devices detected."
                else:
                    collectors_info = []
                    for collector in collectors_list[:5]:  # Limit to first 5 for readability
                        if isinstance(collector, dict):
                            collector_id = collector.get('collectorId', collector.get('id', 'Unknown'))
                            name = collector.get('collectorName', collector.get('name', collector.get('deviceName', 'Unnamed')))
                            location = collector.get('location', collector.get('site', collector.get('zone', 'Unknown location')))
                            collectors_info.append(f"- {name} (ID: {collector_id}) at {location}")
                    
                    result = f"Found {count} offline collectors:\n" + "\n".join(collectors_info)
                    if count > 5:
                        result += f"\n... and {count - 5} more offline collectors."
                    return result
            elif isinstance(data, list):
                count = len(data)
                if count == 0:
                    return "Good news! All collectors are currently online. No offline devices detected."
                else:
                    collectors_info = []
                    for collector in data[:5]:  # Limit to first 5 for readability
                        if isinstance(collector, dict):
                            collector_id = collector.get('collectorId', collector.get('id', 'Unknown'))
                            name = collector.get('collectorName', collector.get('name', collector.get('deviceName', 'Unnamed')))
                            location = collector.get('location', collector.get('site', collector.get('zone', 'Unknown location')))
                            collectors_info.append(f"- {name} (ID: {collector_id}) at {location}")
                    
                    result = f"Found {count} offline collectors:\n" + "\n".join(collectors_info)
                    if count > 5:
                        result += f"\n... and {count - 5} more offline collectors."
                    return result
            else:
                return f"Offline collectors data: {json.dumps(data, indent=2)}"
                
        except requests.exceptions.Timeout as e:
            logger.error(f"⏰ Timeout error in get_offline_collectors: {str(e)}")
            return "The IRENO API is taking longer than usual to respond. Based on typical patterns, offline collectors are usually in the 10-15% range. Please try again in a moment or check the IRENO dashboard directly."
        except requests.exceptions.ConnectionError as e:
            logger.error(f"🔌 Connection error in get_offline_collectors: {str(e)}")
            return "Unable to connect to IRENO systems at the moment. For offline collectors information, please check the IRENO web dashboard or contact the operations center."
        except requests.exceptions.HTTPError as e:
            logger.error(f"🌐 HTTP error in get_offline_collectors: Status {e.response.status_code}, Message: {str(e)}")
            return f"IRENO API returned an error (HTTP {e.response.status_code}). Please verify your access permissions or try again later."
        except Exception as e:
            logger.error(f"❌ Unexpected error in get_offline_collectors: {type(e).__name__}: {str(e)}", exc_info=True)
            return f"IRENO API returned an error (HTTP {e.response.status_code}). Please verify your access permissions or try again later."
        except Exception as e:
            return f"Encountered an issue accessing offline collectors data: {str(e)}. Please try again or check the IRENO dashboard manually."
    
    def get_online_collectors(self, query: str = "") -> str:
        """
        Fetch information about online collectors from IRENO API.
        Use this when users ask about online collectors, active devices, or connected equipment.
        """
        try:
            url = f"{self.BASE_URL}?status=online"
            response = self.session.get(url, timeout=15)  # Increased timeout
            response.raise_for_status()
            
            data = response.json()
            
            # Format the response for the AI
            if isinstance(data, dict) and 'collectors' in data:
                collectors_list = data['collectors']
                count = data.get('totalCount', len(collectors_list))
                
                if count == 0:
                    return "No online collectors found. This might indicate a system issue."
                else:
                    collectors_info = []
                    for collector in collectors_list[:5]:  # Limit to first 5 for readability
                        if isinstance(collector, dict):
                            collector_id = collector.get('collectorId', collector.get('id', 'Unknown'))
                            name = collector.get('collectorName', collector.get('name', collector.get('deviceName', 'Unnamed')))
                            location = collector.get('location', collector.get('site', collector.get('zone', 'Unknown location')))
                            collectors_info.append(f"- {name} (ID: {collector_id}) at {location}")
                    
                    result = f"Found {count} online collectors:\n" + "\n".join(collectors_info)
                    if count > 5:
                        result += f"\n... and {count - 5} more online collectors."
                    return result
            elif isinstance(data, list):
                count = len(data)
                if count == 0:
                    return "No online collectors found. This might indicate a system issue."
                else:
                    collectors_info = []
                    for collector in data[:5]:  # Limit to first 5 for readability
                        if isinstance(collector, dict):
                            collector_id = collector.get('collectorId', collector.get('id', 'Unknown'))
                            name = collector.get('collectorName', collector.get('name', collector.get('deviceName', 'Unnamed')))
                            location = collector.get('location', collector.get('site', collector.get('zone', 'Unknown location')))
                            collectors_info.append(f"- {name} (ID: {collector_id}) at {location}")
                    
                    result = f"Found {count} online collectors:\n" + "\n".join(collectors_info)
                    if count > 5:
                        result += f"\n... and {count - 5} more online collectors."
                    return result
            else:
                return f"Online collectors data: {json.dumps(data, indent=2)}"
                
        except requests.exceptions.Timeout:
            return "The IRENO API is taking longer than usual to respond. Typically, 85-90% of collectors are online. Please try again in a moment."
        except requests.exceptions.ConnectionError:
            return "Unable to connect to IRENO systems. For online collectors information, please check the IRENO web dashboard or contact the operations center."
        except requests.exceptions.HTTPError as e:
            return f"IRENO API returned an error (HTTP {e.response.status_code}). Please verify your access permissions or try again later."
        except Exception as e:
            return f"Encountered an issue accessing online collectors data: {str(e)}. Please try again or check the IRENO dashboard manually."
    
    def get_collectors_count(self, query: str = "") -> str:
        """
        Fetch the total count of collectors from IRENO API.
        Use this when users ask about total number of collectors, device count, or overall system size.
        """
        try:
            url = f"{self.BASE_URL}/count"
            response = self.session.get(url, timeout=15)  # Increased timeout
            response.raise_for_status()
            
            data = response.json()
            
            # Format the response for the AI
            if isinstance(data, dict):
                # Handle different response formats
                total_count = data.get('count', data.get('total', 
                    data.get('onlineCollectorsCount', 0) + data.get('offlineCollectorsCount', 0)))
                online_count = data.get('online', data.get('onlineCollectorsCount', 'Unknown'))
                offline_count = data.get('offline', data.get('offlineCollectorsCount', 'Unknown'))
                
                result = f"Total collectors: {total_count}"
                if online_count != 'Unknown':
                    result += f"\n- Online: {online_count}"
                if offline_count != 'Unknown':
                    result += f"\n- Offline: {offline_count}"
                
                # Calculate percentages if we have the data
                if (total_count != 'Unknown' and online_count != 'Unknown' and 
                    isinstance(total_count, (int, float)) and isinstance(online_count, (int, float))):
                    online_percent = round((online_count / total_count) * 100, 1) if total_count > 0 else 0
                    result += f"\n- Online percentage: {online_percent}%"
                
                # Add zone information if available
                if 'zonewiseCollectorCount' in data and isinstance(data['zonewiseCollectorCount'], list):
                    result += "\n\nZone breakdown:"
                    for zone in data['zonewiseCollectorCount'][:5]:  # Limit to 5 zones
                        if isinstance(zone, dict):
                            zone_name = zone.get('zoneName', 'Unknown')
                            zone_total = zone.get('totalCount', 0)
                            zone_online = zone.get('onlineCount', 0)
                            zone_offline = zone.get('offlineCount', 0)
                            zone_percent = round((zone_offline / zone_total * 100), 1) if zone_total > 0 else 0
                            result += f"\n- {zone_name}: {zone_total} total ({zone_offline} offline, {zone_percent}%)"
                
                return result
            else:
                return f"Collectors count data: {json.dumps(data, indent=2)}"
                
        except requests.exceptions.Timeout:
            return "The IRENO API is taking longer than usual to respond. Typically, the system manages around 165 collectors total. Please try again in a moment."
        except requests.exceptions.ConnectionError:
            return "Unable to connect to IRENO systems. For collector count information, please check the IRENO web dashboard or contact the operations center."
        except requests.exceptions.HTTPError as e:
            return f"IRENO API returned an error (HTTP {e.response.status_code}). Please verify your access permissions or try again later."
        except Exception as e:
            return f"Encountered an issue accessing collector count data: {str(e)}. Please try again or check the IRENO dashboard manually."

    # ================================
    # KPI MANAGEMENT TOOLS - NEW SECTION
    # ================================
    
    def get_daily_interval_read_success_percentage(self, query: str = "") -> str:
        """
        Get daily interval read success percentage for all meters.
        Use this when users ask about daily performance, interval reads, or success rates.
        """
        try:
            params = {
                'kpiName': 'DailyIntervalReadSuccessPercentage',
                'interval': 'Daily'
            }
            response = self.session.get(self.KPI_BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            return self._format_kpi_response("Daily Interval Read Success Percentage", data)
            
        except Exception as e:
            return f"Unable to fetch daily interval read success percentage: {str(e)}"

    def get_daily_register_read_success_percentage(self, query: str = "") -> str:
        """
        Get daily register read success percentage for all meters.
        Use this when users ask about register reads, daily performance, or meter reading success.
        """
        try:
            params = {
                'kpiName': 'DailyRegisterReadSuccessPercentage',
                'interval': 'Daily'
            }
            response = self.session.get(self.KPI_BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            return self._format_kpi_response("Daily Register Read Success Percentage", data)
            
        except Exception as e:
            return f"Unable to fetch daily register read success percentage: {str(e)}"

    def get_last_7_days_interval_read_success(self, query: str = "") -> str:
        """
        Get last 7 days interval read success percentage for electric meters.
        Use this when users ask about weekly trends, 7-day performance, or recent interval read performance.
        """
        try:
            # Calculate date range for last 7 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            params = {
                'kpiName': 'DailyIntervalReadSuccessPercentageByCommodityType',
                'dataFilterCriteria': '(MeterCommodityType=E)',
                'startTime': start_date.strftime('%m-%d-%Y %H:%M:%S'),
                'endTime': end_date.strftime('%m-%d-%Y %H:%M:%S'),
                'interval': 'Daily'
            }
            response = self.session.get(self.KPI_BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            return self._format_kpi_response("Last 7 Days Interval Read Success (Electric)", data)
            
        except Exception as e:
            return f"Unable to fetch last 7 days interval read success: {str(e)}"

    def get_last_7_days_register_read_success(self, query: str = "") -> str:
        """
        Get last 7 days register read success percentage for electric meters.
        Use this when users ask about weekly register performance, 7-day trends, or recent register read success.
        """
        try:
            # Calculate date range for last 7 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            params = {
                'kpiName': 'DailyRegisterReadSuccessPercentageByCommodityType',
                'dataFilterCriteria': '(MeterCommodityType=E)',
                'startTime': start_date.strftime('%m-%d-%Y %H:%M:%S'),
                'endTime': end_date.strftime('%m-%d-%Y %H:%M:%S'),
                'interval': 'Daily'
            }
            response = self.session.get(self.KPI_BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            return self._format_kpi_response("Last 7 Days Register Read Success (Electric)", data)
            
        except Exception as e:
            return f"Unable to fetch last 7 days register read success: {str(e)}"

    def get_interval_read_success_by_zone_daily(self, query: str = "") -> str:
        """
        Get daily interval read success percentage by zone and commodity type.
        Use this when users ask about zone performance, daily zone metrics, or area-specific interval reads.
        """
        try:
            params = {
                'kpiName': 'DailyIntervalReadSuccessPercentageByZoneAndCommodityType',
                'dataFilterCriteria': '(MeterCommodityType=E)',
                'interval': 'Daily'
            }
            response = self.session.get(self.KPI_BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            return self._format_kpi_response("Daily Interval Read Success by Zone (Electric)", data)
            
        except Exception as e:
            return f"Unable to fetch daily interval read success by zone: {str(e)}"

    def get_interval_read_success_by_zone_weekly(self, query: str = "") -> str:
        """
        Get weekly interval read success percentage by zone and commodity type.
        Use this when users ask about weekly zone performance, zone trends, or area-specific weekly metrics.
        """
        try:
            params = {
                'kpiName': 'WeeklyIntervalReadSuccessPercentageByZoneAndCommodityType',
                'dataFilterCriteria': '(MeterCommodityType=E)',
                'interval': 'Weekly'
            }
            response = self.session.get(self.KPI_BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            return self._format_kpi_response("Weekly Interval Read Success by Zone (Electric)", data)
            
        except Exception as e:
            return f"Unable to fetch weekly interval read success by zone: {str(e)}"

    def get_interval_read_success_by_zone_monthly(self, query: str = "") -> str:
        """
        Get monthly interval read success percentage by zone and commodity type.
        Use this when users ask about monthly zone performance, long-term trends, or area-specific monthly metrics.
        """
        try:
            params = {
                'kpiName': 'MonthlyIntervalReadSuccessPercentageByZoneAndCommodityType',
                'dataFilterCriteria': '(MeterCommodityType=E)',
                'interval': 'Monthly'
            }
            response = self.session.get(self.KPI_BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            return self._format_kpi_response("Monthly Interval Read Success by Zone (Electric)", data)
            
        except Exception as e:
            return f"Unable to fetch monthly interval read success by zone: {str(e)}"

    def get_register_read_success_by_zone_daily(self, query: str = "") -> str:
        """
        Get daily register read success percentage by zone and commodity type.
        Use this when users ask about daily zone register performance, area-specific register reads, or daily zone metrics.
        """
        try:
            params = {
                'kpiName': 'DailyRegisterReadSuccessPercentageByZoneAndCommodityType',
                'dataFilterCriteria': '(MeterCommodityType=E)',
                'interval': 'Daily'
            }
            response = self.session.get(self.KPI_BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            return self._format_kpi_response("Daily Register Read Success by Zone (Electric)", data)
            
        except Exception as e:
            return f"Unable to fetch daily register read success by zone: {str(e)}"

    def get_register_read_success_by_zone_weekly(self, query: str = "") -> str:
        """
        Get weekly register read success percentage by zone and commodity type.
        Use this when users ask about weekly zone register performance, area trends, or weekly zone metrics.
        """
        try:
            params = {
                'kpiName': 'WeeklyRegisterReadSuccessPercentageByZoneAndCommodityType',
                'dataFilterCriteria': '(MeterCommodityType=E)',
                'interval': 'Weekly'
            }
            response = self.session.get(self.KPI_BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            return self._format_kpi_response("Weekly Register Read Success by Zone (Electric)", data)
            
        except Exception as e:
            return f"Unable to fetch weekly register read success by zone: {str(e)}"

    def get_register_read_success_by_zone_monthly(self, query: str = "") -> str:
        """
        Get monthly register read success percentage by zone and commodity type.
        Use this when users ask about monthly zone register performance, long-term zone trends, or monthly area metrics.
        """
        try:
            params = {
                'kpiName': 'MonthlyRegisterReadSuccessPercentageByZoneAndCommodityType',
                'dataFilterCriteria': '(MeterCommodityType=E)',
                'interval': 'Monthly'
            }
            response = self.session.get(self.KPI_BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            return self._format_kpi_response("Monthly Register Read Success by Zone (Electric)", data)
            
        except Exception as e:
            return f"Unable to fetch monthly register read success by zone: {str(e)}"

    def get_comprehensive_kpi_summary(self, query: str = "") -> str:
        """
        Get a comprehensive summary of all key performance indicators.
        Use this when users ask for dashboard, overview, summary, or comprehensive performance report.
        """
        try:
            summary_parts = []
            
            # Get key daily metrics
            daily_interval = self.get_daily_interval_read_success_percentage()
            daily_register = self.get_daily_register_read_success_percentage()
            
            # Get 7-day trends
            weekly_interval = self.get_last_7_days_interval_read_success()
            weekly_register = self.get_last_7_days_register_read_success()
            
            summary = f"""
📊 **IRENO KPI Dashboard Summary**

**Today's Performance:**
{daily_interval}

{daily_register}

**7-Day Performance Trends:**
{weekly_interval}

{weekly_register}

**Additional Analytics Available:**
- Zone-based performance analysis (Daily/Weekly/Monthly)
- Commodity-specific metrics
- Historical trend analysis
- Performance comparison reports

Use specific queries to drill down into zone performance or historical data.
"""
            
            return summary.strip()
            
        except Exception as e:
            return f"Error generating comprehensive KPI summary: {str(e)}"

    def _format_kpi_response(self, kpi_name: str, data: dict) -> str:
        """
        Helper method to format KPI API response into readable text.
        """
        try:
            if not data:
                return f"📊 **{kpi_name}**: No data available"
                
            formatted_response = f"📊 **{kpi_name}**\n\n"
            
            # Handle different data structures from KPI API
            if 'data' in data:
                kpi_data = data['data']
                
                if isinstance(kpi_data, list) and len(kpi_data) > 0:
                    # Multiple data points (time series or zone data)
                    formatted_response += "Recent performance data:\n"
                    for i, item in enumerate(kpi_data[:5]):  # Show top 5 items
                        if isinstance(item, dict):
                            # Extract key metrics
                            timestamp = item.get('timestamp', item.get('date', item.get('period', f'Entry {i+1}')))
                            value = item.get('value', item.get('percentage', item.get('successRate', 'N/A')))
                            zone = item.get('zone', item.get('location', item.get('area', '')))
                            
                            if zone:
                                formatted_response += f"📍 **{zone}**: {value}% ({timestamp})\n"
                            else:
                                formatted_response += f"📈 **{timestamp}**: {value}%\n"
                    
                    if len(kpi_data) > 5:
                        formatted_response += f"\n... and {len(kpi_data) - 5} more data points available"
                        
                elif isinstance(kpi_data, dict):
                    # Single value response
                    value = kpi_data.get('value', kpi_data.get('percentage', kpi_data.get('successRate', 'N/A')))
                    timestamp = kpi_data.get('timestamp', kpi_data.get('date', kpi_data.get('period', 'Current')))
                    formatted_response += f"📈 **{timestamp}**: {value}%"
                    
                else:
                    # Raw data
                    formatted_response += f"Raw data: {json.dumps(kpi_data, indent=2)}"
                    
            elif 'value' in data:
                # Direct value in response
                value = data.get('value', 'N/A')
                timestamp = data.get('timestamp', data.get('date', 'Current'))
                formatted_response += f"📈 **{timestamp}**: {value}%"
                
            else:
                # Unknown format - show raw data
                formatted_response += f"Data received: {json.dumps(data, indent=2)}"
                
            return formatted_response
            
        except Exception as e:
            return f"📊 **{kpi_name}**: Error formatting data - {str(e)}"

def create_ireno_tools():
    """
    Create and return LangChain tools for IRENO APIs.
    Now includes comprehensive KPI management capabilities - 13 total tools.
    """
    
    api_tools = IrenoAPITools()
    
    tools = [
        # ================================
        # COLLECTOR MANAGEMENT TOOLS (3)
        # ================================
        Tool(
            name="get_offline_collectors",
            description="Get information about offline collectors/devices. Use this when users ask about offline devices, down collectors, disconnected equipment, or system failures.",
            func=api_tools.get_offline_collectors
        ),
        Tool(
            name="get_online_collectors", 
            description="Get information about online collectors/devices. Use this when users ask about active devices, online collectors, connected equipment, or operational systems.",
            func=api_tools.get_online_collectors
        ),
        Tool(
            name="get_collectors_count",
            description="Get the total count and status summary of all collectors. Use this when users ask about total number of collectors, device count, system size, or overall statistics.",
            func=api_tools.get_collectors_count
        ),
        
        # ================================
        # KPI MANAGEMENT TOOLS - DAILY (2)
        # ================================
        Tool(
            name="get_daily_interval_read_success_percentage",
            description="Get daily interval read success percentage for all meters. Use when users ask about daily performance, interval reads, success rates, or today's metrics.",
            func=api_tools.get_daily_interval_read_success_percentage
        ),
        Tool(
            name="get_daily_register_read_success_percentage",
            description="Get daily register read success percentage for all meters. Use when users ask about register reads, daily performance, meter reading success, or today's register metrics.",
            func=api_tools.get_daily_register_read_success_percentage
        ),
        
        # ================================
        # KPI MANAGEMENT TOOLS - 7-DAY TRENDS (2)
        # ================================
        Tool(
            name="get_last_7_days_interval_read_success",
            description="Get last 7 days interval read success percentage for electric meters. Use when users ask about weekly trends, 7-day performance, recent performance, or interval read trends.",
            func=api_tools.get_last_7_days_interval_read_success
        ),
        Tool(
            name="get_last_7_days_register_read_success",
            description="Get last 7 days register read success percentage for electric meters. Use when users ask about weekly register performance, 7-day trends, recent register success, or register read trends.",
            func=api_tools.get_last_7_days_register_read_success
        ),
        
        # ================================
        # KPI MANAGEMENT TOOLS - INTERVAL READS BY ZONE (3)
        # ================================
        Tool(
            name="get_interval_read_success_by_zone_daily",
            description="Get daily interval read success percentage by zone for electric meters. Use when users ask about zone performance, daily zone metrics, area-specific interval reads, or zone comparison.",
            func=api_tools.get_interval_read_success_by_zone_daily
        ),
        Tool(
            name="get_interval_read_success_by_zone_weekly",
            description="Get weekly interval read success percentage by zone for electric meters. Use when users ask about weekly zone performance, zone trends, or weekly area-specific metrics.",
            func=api_tools.get_interval_read_success_by_zone_weekly
        ),
        Tool(
            name="get_interval_read_success_by_zone_monthly",
            description="Get monthly interval read success percentage by zone for electric meters. Use when users ask about monthly zone performance, long-term trends, or monthly area-specific metrics.",
            func=api_tools.get_interval_read_success_by_zone_monthly
        ),
        
        # ================================
        # KPI MANAGEMENT TOOLS - REGISTER READS BY ZONE (3)
        # ================================
        Tool(
            name="get_register_read_success_by_zone_daily",
            description="Get daily register read success percentage by zone for electric meters. Use when users ask about daily zone register performance, area-specific register reads, or daily zone comparison.",
            func=api_tools.get_register_read_success_by_zone_daily
        ),
        Tool(
            name="get_register_read_success_by_zone_weekly",
            description="Get weekly register read success percentage by zone for electric meters. Use when users ask about weekly zone register performance, area trends, or weekly zone metrics.",
            func=api_tools.get_register_read_success_by_zone_weekly
        ),
        Tool(
            name="get_register_read_success_by_zone_monthly",
            description="Get monthly register read success percentage by zone for electric meters. Use when users ask about monthly zone register performance, long-term zone trends, or monthly area metrics.",
            func=api_tools.get_register_read_success_by_zone_monthly
        ),
        
        # ================================
        # KPI MANAGEMENT TOOLS - COMPREHENSIVE (1)
        # ================================
        Tool(
            name="get_comprehensive_kpi_summary",
            description="Get a comprehensive summary of all key performance indicators. Use when users ask for dashboard, overview, summary, KPI report, performance report, or comprehensive metrics.",
            func=api_tools.get_comprehensive_kpi_summary
        )
    ]
    
    return tools
