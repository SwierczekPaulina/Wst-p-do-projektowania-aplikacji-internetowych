window.addEventListener('load', function() {
    fetchAndDisplayTeamMembers();
});

function fetchAndDisplayTeamMembers() {
    // Fetch the team members list from the server
    fetch('/data', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())  // Parse the response as JSON
    .then(data => {
        // Clear the current team members list
        const teamMembersList = document.getElementById('team-members');
        teamMembersList.innerHTML = ''; // Clear the list

        // Re-add all team members from the server data
        data.forEach(member => {
            addTeamMember(member.first_name, member.last_name, member.role, member.id);
        });
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

document.getElementById('team-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(this); // Create a FormData object from the form
    // Convert form data to a plain JavaScript object
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Send data as JSON to the server
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Sending JSON
        },
        body: JSON.stringify(data) // Convert the data object to JSON
    })
    .then(response => {
        if (response.ok && data.privacy_policy == "on") {
            // Re-fetch and display the updated team members list after the form is submitted
            fetchAndDisplayTeamMembers();
        }
        this.reset();
    });
});

function addTeamMember(firstName, lastName, role, id) {
    const teamMembersList = document.getElementById('team-members');

    const listItem = document.createElement('li');
    listItem.classList.add('team-members-item');

    const info = document.createElement('div');
    info.innerHTML = `<p><strong>${firstName} ${lastName}</strong></p><p class='gray-text'>${role}</p>`;

    const deleteButton = document.createElement('button');
    deleteButton.classList.add('delete-button');
    deleteButton.innerHTML = '🗑️';

    // When the delete button is clicked, send a DELETE request
    deleteButton.addEventListener('click', function () {
        fetch(`/delete/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                // Re-fetch and display the updated team members list after deletion
                fetchAndDisplayTeamMembers();
            }
        })
        .catch(error => {
            console.error('Error deleting member:', error);
        });
    });

    listItem.appendChild(info);
    listItem.appendChild(deleteButton);
    teamMembersList.appendChild(listItem);
}
