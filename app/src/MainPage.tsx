import React from 'react';
import SearchBar from './SearchBar';
import ContentSection from './ContentSection';
import { Link } from 'react-router-dom';

const MainPage = () => {
    const regions = ['홍대', '강남', '건대'];

    return (
        <div>
            <SearchBar />
            <div className="text-center my-4">
                {regions.map(region => (
                    <Link 
                        to={`/search?region=${region}`} 
                        key={region}
                        className="inline-block bg-gray-200 rounded-full px-4 py-2 text-sm font-semibold text-gray-700 mr-2 mb-2"
                    >
                        #{region}
                    </Link>
                ))}
            </div>
            <div className="mt-8">
                <ContentSection title="인기 테마 TOP 10" />
                <ContentSection title="이번 주 신규 테마" />
                <ContentSection title="지역별 추천 카페" />
            </div>
        </div>
    );
};

export default MainPage;