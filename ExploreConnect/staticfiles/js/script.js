document.addEventListener('DOMContentLoaded', function() {
    const continentItems = document.querySelectorAll('.continent-item');

    continentItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const continent = this.getAttribute('data-continent');
            const countryMenu = this.nextElementSibling;

            // Clear previous countries
            countryMenu.innerHTML = '';

            // Fetch countries for the selected continent
            fetch(`/get-countries/?continent=${continent}`)
                .then(response => response.json())
                .then(data => {
                    if (data.countries.length > 0) {
                        data.countries.forEach(country => {
                            const li = document.createElement('li');
                            li.innerHTML = `<a href="/destination/${country.id}">${country.name}</a>`;
                            countryMenu.appendChild(li);
                        });
                    } else {
                        countryMenu.innerHTML = '<li>No countries available.</li>';
                    }
                })
                .catch(error => console.error('Error fetching countries:', error));
        });
    });
});
