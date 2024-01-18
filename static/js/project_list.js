document.addEventListener('DOMContentLoaded', function () {
    const filterActive = document.getElementById('filterActive');
    const filterCompleted = document.getElementById('filterCompleted');
    const filterAllProjects = document.getElementById('filterAllProjects');
    const projectTable = document.getElementById('projectTable');

    setFilterActive();

    filterActive.addEventListener('click', setFilterActive);
    filterCompleted.addEventListener('click', setFilterCompleted);
    filterAllProjects.addEventListener('click', setFilterAllProjects);

    function setFilterActive() {
        showActiveProjects();
        setActiveButton(filterActive);
        removeActiveButton(filterCompleted);
        removeActiveButton(filterAllProjects);
    }

    function setFilterCompleted() {
        hideActiveProjects();
        setActiveButton(filterCompleted);
        removeActiveButton(filterActive);
        removeActiveButton(filterAllProjects);
    }

    function setFilterAllProjects() {
        showAllProjects();
        setActiveButton(filterAllProjects);
        removeActiveButton(filterActive);
        removeActiveButton(filterCompleted);
    }

    function showActiveProjects() {
        Array.from(projectTable.getElementsByClassName('complete-project')).forEach((row, index) => {
            row.style.display = 'none';
            row.firstElementChild.innerText = index + 1;
        });
        Array.from(projectTable.getElementsByClassName('active-project')).forEach((row, index) => {
            row.style.display = '';
            row.firstElementChild.innerText = index + 1;
        });
    }

    function hideActiveProjects() {
        Array.from(projectTable.getElementsByClassName('active-project')).forEach((row, index) => {
            row.style.display = 'none';
            row.firstElementChild.innerText = index + 1;
        });
        Array.from(projectTable.getElementsByClassName('complete-project')).forEach((row, index) => {
            row.style.display = '';
            row.firstElementChild.innerText = index + 1;
        });
    }

    function showAllProjects() {
        Array.from(projectTable.getElementsByTagName('tr')).forEach((row, index) => {
            row.style.display = '';
            row.firstElementChild.innerText = index + 1;
        });
    }

    function setActiveButton(button) {
        button.classList.add('active');
    }

    function removeActiveButton(button) {
        button.classList.remove('active');
    }
});
