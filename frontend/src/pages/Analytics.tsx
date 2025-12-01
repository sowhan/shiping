import React, { useState, useEffect } from 'react';
import {
  BarChart3, TrendingUp, TrendingDown, DollarSign, Clock,
  Ship, Route, Percent, Activity, Calendar
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent, Loading, Button } from '../components/ui';

interface AnalyticsMetric {
  label: string;
  value: string | number;
  change?: number;
  trend?: 'up' | 'down' | 'neutral';
  icon: React.ReactNode;
}

interface TimeSeriesData {
  date: string;
  calculations: number;
  avgTime: number;
  cacheHits: number;
}

/**
 * Analytics page for performance metrics and business intelligence.
 */
export const Analytics: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d'>('7d');
  const [metrics, setMetrics] = useState<AnalyticsMetric[]>([]);
  const [timeSeriesData, setTimeSeriesData] = useState<TimeSeriesData[]>([]);

  useEffect(() => {
    // Simulate loading analytics data
    setTimeout(() => {
      setMetrics([
        {
          label: 'Total Calculations',
          value: '12,847',
          change: 12.5,
          trend: 'up',
          icon: <Route className="w-5 h-5 text-blue-600" />
        },
        {
          label: 'Average Calc Time',
          value: '342ms',
          change: -8.3,
          trend: 'up',
          icon: <Clock className="w-5 h-5 text-green-600" />
        },
        {
          label: 'Cache Hit Ratio',
          value: '96.2%',
          change: 2.1,
          trend: 'up',
          icon: <Percent className="w-5 h-5 text-purple-600" />
        },
        {
          label: 'Cost Savings',
          value: '$1.2M',
          change: 15.8,
          trend: 'up',
          icon: <DollarSign className="w-5 h-5 text-emerald-600" />
        }
      ]);

      setTimeSeriesData([
        { date: 'Mon', calculations: 1580, avgTime: 320, cacheHits: 94 },
        { date: 'Tue', calculations: 1820, avgTime: 345, cacheHits: 95 },
        { date: 'Wed', calculations: 2100, avgTime: 310, cacheHits: 96 },
        { date: 'Thu', calculations: 1950, avgTime: 355, cacheHits: 95 },
        { date: 'Fri', calculations: 2250, avgTime: 340, cacheHits: 97 },
        { date: 'Sat', calculations: 1200, avgTime: 295, cacheHits: 98 },
        { date: 'Sun', calculations: 947, avgTime: 285, cacheHits: 98 }
      ]);

      setLoading(false);
    }, 1000);
  }, [timeRange]);

  if (loading) {
    return (
      <div className="min-h-[400px] flex items-center justify-center">
        <Loading size="lg" variant="spinner" text="Loading analytics..." />
      </div>
    );
  }

  const maxCalculations = Math.max(...timeSeriesData.map(d => d.calculations));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-500 mt-1">Performance metrics and business intelligence</p>
        </div>
        <div className="flex gap-2">
          {(['24h', '7d', '30d'] as const).map((range) => (
            <Button
              key={range}
              variant={timeRange === range ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setTimeRange(range)}
            >
              {range === '24h' ? 'Last 24h' : range === '7d' ? 'Last 7 days' : 'Last 30 days'}
            </Button>
          ))}
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((metric, index) => (
          <Card key={index}>
            <CardContent className="pt-4">
              <div className="flex items-start justify-between">
                <div className="p-2 bg-gray-100 rounded-lg">
                  {metric.icon}
                </div>
                {metric.change !== undefined && (
                  <span className={`flex items-center gap-1 text-sm font-medium ${
                    metric.trend === 'up' && metric.change > 0 ? 'text-green-600' :
                    metric.trend === 'down' || metric.change < 0 ? 'text-red-600' :
                    'text-gray-500'
                  }`}>
                    {metric.change > 0 ? (
                      <TrendingUp className="w-4 h-4" />
                    ) : (
                      <TrendingDown className="w-4 h-4" />
                    )}
                    {Math.abs(metric.change)}%
                  </span>
                )}
              </div>
              <div className="mt-4">
                <p className="text-2xl font-bold text-gray-900">{metric.value}</p>
                <p className="text-sm text-gray-500 mt-1">{metric.label}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Calculations Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-gray-400" />
              Route Calculations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-end justify-between gap-2">
              {timeSeriesData.map((data, index) => (
                <div key={index} className="flex-1 flex flex-col items-center gap-2">
                  <div
                    className="w-full bg-maritime-blue/80 rounded-t-lg transition-all hover:bg-maritime-blue"
                    style={{ height: `${(data.calculations / maxCalculations) * 200}px` }}
                  />
                  <span className="text-xs text-gray-500">{data.date}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Performance Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-gray-400" />
              Performance Metrics
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {/* Average Response Time */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Average Response Time</span>
                  <span className="text-sm font-medium text-gray-900">342ms</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-500 h-2 rounded-full"
                    style={{ width: `${Math.min(100, (1 - 342 / 500) * 100)}%` }}
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">Target: &lt;500ms ({Math.round((1 - 342 / 500) * 100)}% of target achieved)</p>
              </div>

              {/* Cache Hit Ratio */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Cache Hit Ratio</span>
                  <span className="text-sm font-medium text-gray-900">96.2%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-purple-500 h-2 rounded-full"
                    style={{ width: '96.2%' }}
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">Target: &gt;95% ✓</p>
              </div>

              {/* Success Rate */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Success Rate</span>
                  <span className="text-sm font-medium text-gray-900">99.4%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-500 h-2 rounded-full"
                    style={{ width: '99.4%' }}
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">Target: &gt;98% ✓</p>
              </div>

              {/* Uptime */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">System Uptime</span>
                  <span className="text-sm font-medium text-gray-900">99.97%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-emerald-500 h-2 rounded-full"
                    style={{ width: '99.97%' }}
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">Target: &gt;99.9% ✓</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Popular Routes */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Route className="w-5 h-5 text-gray-400" />
            Most Popular Routes
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { route: 'SGSIN → NLRTM', count: 2847, percentage: 22 },
              { route: 'CNSHA → USLAX', count: 2156, percentage: 17 },
              { route: 'HKHKG → DEHAM', count: 1893, percentage: 15 },
              { route: 'AEJEA → BEANR', count: 1654, percentage: 13 },
              { route: 'JPNGO → USPNY', count: 1432, percentage: 11 }
            ].map((item, index) => (
              <div key={index} className="flex items-center gap-4">
                <span className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center text-sm font-medium text-gray-600">
                  {index + 1}
                </span>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-gray-900">{item.route}</span>
                    <span className="text-sm text-gray-500">{item.count.toLocaleString()} calculations</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-1.5">
                    <div
                      className="bg-maritime-blue h-1.5 rounded-full"
                      style={{ width: `${item.percentage}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Analytics;
