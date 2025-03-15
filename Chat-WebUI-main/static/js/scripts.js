function updateSEOInterface(data, container) {
    switch (data.type) {
        case 'titles':
            const titlesContainer = container.querySelector('.titles-container');
            titlesContainer.innerHTML = `
                <h4>Title Suggestions</h4>
                <ul class="seo-titles-list">
                    ${data.content.map(title => `<li>${title}</li>`).join('')}
                </ul>
            `;
            break;

        case 'description':
            const descriptionContainer = container.querySelector('.description-container');
            descriptionContainer.innerHTML = `
                <h4>Description</h4>
                <div class="seo-description">${data.content}</div>
            `;
            break;

        case 'tags':
            const tagsContainer = container.querySelector('.tags-container');
            tagsContainer.innerHTML = `
                <h4>Tags</h4>
                <div class="seo-tags">${data.content.join(', ')}</div>
            `;
            break;

        case 'hashtags':
            const hashtagsContainer = container.querySelector('.hashtags-container');
            hashtagsContainer.innerHTML = `
                <h4>Hashtags</h4>
                <div class="seo-hashtags">${data.content.join(' ')}</div>
            `;
            break;

        case 'score':
            const scoreContainer = container.querySelector('.score-container');
            scoreContainer.innerHTML = `
                <h4>SEO Score</h4>
                <div class="seo-score">${data.content}/100</div>
            `;
            break;

        case 'analytics':
            const analyticsContainer = container.querySelector('.analytics-container');
            analyticsContainer.innerHTML = `
                <h4>Analytics Insights</h4>
                <div class="seo-analytics">${data.content}</div>
            `;
            break;

        case 'top_videos':
            const topVideosContainer = container.querySelector('.top-videos-container');
            // Call the displayTopVideos function with the video data and the container
            displayTopVideos(data.content, topVideosContainer);
            break;

        default:
            console.log('Unknown SEO data type:', data.type);
    }
}
