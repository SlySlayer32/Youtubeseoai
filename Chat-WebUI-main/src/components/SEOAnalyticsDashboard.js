import React, { useState, useEffect } from 'react';
import { Line, Bar, Pie } from 'react-chartjs-2';
import { Card, Row, Col, Table, Input, DatePicker, Button, Select } from 'antd';
import moment from 'moment';

const { RangePicker } = DatePicker;
const { Option } = Select;

const SEOAnalyticsDashboard = () => {
    const [analytics, setAnalytics] = useState({
        videoPerformance: [],
        keywordPerformance: [],
        titleEffectiveness: [],
        viewsOverTime: [],
        engagementMetrics: {}
    });
    const [dateRange, setDateRange] = useState([moment().subtract(30, 'days'), moment()]);
    const [selectedVideos, setSelectedVideos] = useState([]);
    const [videos, setVideos] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchVideos();
    }, []);

    useEffect(() => {
        if (selectedVideos.length > 0) {
            fetchAnalytics();
        }
    }, [selectedVideos, dateRange]);

    const fetchVideos = async () => {
        try {
            const response = await fetch('/api/videos');
            const data = await response.json();
            setVideos(data);
        } catch (error) {
            console.error('Error fetching videos:', error);
        }
    };

    const fetchAnalytics = async () => {
        setLoading(true);
        try {
            const [startDate, endDate] = dateRange;
            const response = await fetch('/api/analytics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    videoIds: selectedVideos,
                    startDate: startDate.format('YYYY-MM-DD'),
                    endDate: endDate.format('YYYY-MM-DD')
                })
            });

            const data = await response.json();
            setAnalytics(data);
        } catch (error) {
            console.error('Error fetching analytics:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleDateRangeChange = (dates) => {
        setDateRange(dates);
    };

    const handleVideoSelection = (value) => {
        setSelectedVideos(value);
    };

    return (
        <div className="seo-analytics-dashboard">
            <h1>YouTube SEO Analytics Dashboard</h1>

            <Card className="filters-card">
                <Row gutter={16}>
                    <Col span={12}>
                        <label>Select Videos:</label>
                        <Select
                            mode="multiple"
                            style={{ width: '100%' }}
                            placeholder="Select videos to analyze"
                            value={selectedVideos}
                            onChange={handleVideoSelection}
                        >
                            {videos.map(video => (
                                <Option key={video.id} value={video.id}>
                                    {video.title}
                                </Option>
                            ))}
                        </Select>
                    </Col>
                    <Col span={8}>
                        <label>Date Range:</label>
                        <RangePicker
                            value={dateRange}
                            onChange={handleDateRangeChange}
                        />
                    </Col>
                    <Col span={4}>
                        <Button
                            type="primary"
                            onClick={fetchAnalytics}
                            loading={loading}
                            style={{ marginTop: '24px' }}
                        >
                            Update Analytics
                        </Button>
                    </Col>
                </Row>
            </Card>

            <Row gutter={16} className="dashboard-row">
                <Col span={24}>
                    <Card title="Views Over Time" loading={loading}>
                        <Line
                            data={{
                                labels: analytics.viewsOverTime.map(item => item.date),
                                datasets: [
                                    {
                                        label: 'Views',
                                        data: analytics.viewsOverTime.map(item => item.views),
                                        borderColor: 'rgba(75, 192, 192, 1)',
                                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                    }],
                            }}
                            options={{
                                responsive: true,
                                maintainAspectRatio: false,
                                scales: {
                                    x: {
                                        title: {
                                            display: true,
                                            text: 'Date',
                                        },
                                    },
                                    y: {
                                        title: {
                                            display: true,
                                            text: 'Views',
                                        },
                                        beginAtZero: true,
                                    },
                                },
                            }}
                        />
                    </Card>
                </Col>
            </Row>

            <Row gutter={16} className="dashboard-row">
                <Col span={12}>
                    <Card title="Keyword Performance" loading={loading}>
                        <Bar
                            data={{
                                labels: analytics.keywordPerformance.map(item => item.keyword),
                                datasets: [
                                    {
                                        label: 'CTR (%)',
                                        data: analytics.keywordPerformance.map(item => item.ctr * 100),
                                        backgroundColor: 'rgba(153, 102, 255, 0.6)',
                                    },
                                    {
                                        label: 'Avg. Watch Time (min)',
                                        data: analytics.keywordPerformance.map(item => item.avgWatchTime / 60),
                                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                                    }
                                ]
                            }}
                            options={{
                                responsive: true,
                                scales: {
                                    y: {
                                        beginAtZero: true
                                    }
                                }
                            }}
                        />
                    </Card>
                </Col>
                <Col span={12}>
                    <Card title="Title Effectiveness" loading={loading}>
                        <Bar
                            data={{
                                labels: analytics.titleEffectiveness.map(item => item.title.substring(0, 20) + '...'),
                                datasets: [
                                    {
                                        label: 'Impressions',
                                        data: analytics.titleEffectiveness.map(item => item.impressions),
                                        backgroundColor: 'rgba(255, 159, 64, 0.6)',
                                    },
                                    {
                                        label: 'Clicks',
                                        data: analytics.titleEffectiveness.map(item => item.clicks),
                                        backgroundColor: 'rgba(255, 99, 132, 0.6)',
                                    }
                                ]
                            }}
                            options={{
                                responsive: true,
                                scales: {
                                    y: {
                                        beginAtZero: true
                                    }
                                }
                            }}
                        />
                    </Card>
                </Col>
            </Row>

            <Row gutter={16} className="dashboard-row">
                <Col span={8}>
                    <Card title="Engagement Metrics" loading={loading}>
                        <Pie
                            data={{
                                labels: ['Likes', 'Comments', 'Shares', 'Saves'],
                                datasets: [
                                    {
                                        data: [
                                            analytics.engagementMetrics.likes || 0,
                                            analytics.engagementMetrics.comments || 0,
                                            analytics.engagementMetrics.shares || 0,
                                            analytics.engagementMetrics.saves || 0
                                        ],
                                        backgroundColor: [
                                            'rgba(255, 99, 132, 0.6)',
                                            'rgba(54, 162, 235, 0.6)',
                                            'rgba(255, 206, 86, 0.6)',
                                            'rgba(75, 192, 192, 0.6)'
                                        ]
                                    }
                                ]
                            }}
                        />
                    </Card>
                </Col>
                <Col span={16}>
                    <Card title="Video Performance" loading={loading}>
                        <Table
                            dataSource={analytics.videoPerformance}
                            rowKey="videoId"
                            pagination={false}
                            columns={[
                                {
                                    title: 'Video Title',
                                    dataIndex: 'title',
                                    key: 'title',
                                    render: text => text.length > 40 ? text.substring(0, 40) + '...' : text
                                },
                                {
                                    title: 'Views',
                                    dataIndex: 'views',
                                    key: 'views',
                                    sorter: (a, b) => a.views - b.views
                                },
                                {
                                    title: 'CTR (%)',
                                    dataIndex: 'ctr',
                                    key: 'ctr',
                                    render: value => (value * 100).toFixed(2) + '%',
                                    sorter: (a, b) => a.ctr - b.ctr
                                },
                                {
                                    title: 'Avg. Watch Time',
                                    dataIndex: 'avgWatchTime',
                                    key: 'avgWatchTime',
                                    render: value => {
                                        const minutes = Math.floor(value / 60);
                                        const seconds = Math.round(value % 60);
                                        return `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
                                    },
                                    sorter: (a, b) => a.avgWatchTime - b.avgWatchTime
                                },
                                {
                                    title: 'SEO Score',
                                    dataIndex: 'seoScore',
                                    key: 'seoScore',
                                    render: value => `${value}/100`,
                                    sorter: (a, b) => a.seoScore - b.seoScore
                                }
                            ]}
                        />
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default SEOAnalyticsDashboard;
