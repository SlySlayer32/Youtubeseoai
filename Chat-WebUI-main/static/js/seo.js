async function displayTopVideos(keyword, resultsContainer) {
    const baseUrl = document.getElementById('base-url').value.trim().replace(/\/+$/, '');
    try {
        const response = await fetch(`${baseUrl}/api/seo/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                keyword: keyword
            })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let topVideos = null;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const lines = decoder.decode(value).split('\\n');
            for (const line of lines) {
                if (!line.trim()) continue;

                try {
                    const data = JSON.parse(line);
                    if (data.type === 'top_videos') {
                        topVideos = data.data;
                        break;
                    }
                } catch (e) {
                    console.error('Error parsing SSE data:', e);
                }
            }
            if (topVideos) break;
        }

        if (topVideos && topVideos.length > 0) {
            const topVideosContainer = document.createElement('div');
            topVideosContainer.classList.add('top-videos-container');
            topVideosContainer.innerHTML = `
                <h4>Top Related Videos</h4>
                <ul>
                    ${topVideos.map(video => `
                        <li>
                            <a href="${video.url}" target="_blank">${video.title}</a>
                        </li>
                    `).join('')}
                </ul>
            `;
            resultsContainer.appendChild(topVideosContainer);
        } else {
            resultsContainer.innerHTML += '<div class="no-videos">No related videos found.</div>';
        }

    } catch (error) {
        resultsContainer.innerHTML = `<div class="error">Error fetching top videos: ${error.message}</div>`;
    }
}
