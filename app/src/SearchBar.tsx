import React from 'react';

const SearchBar = () => {
    return (
        <div className="text-center p-8 bg-gray-100 rounded-lg">
            <input 
                type="text" 
                placeholder="Search for themes or cafes..." 
                className="w-full max-w-lg p-4 border rounded-full"
            />
        </div>
    );
};

export default SearchBar;
