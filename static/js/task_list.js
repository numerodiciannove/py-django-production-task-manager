document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('.btn-group button');
    const taskTable = document.getElementById('taskTable');
    let activeFilter = 'filterIncomplete';

    hideCompleteRows();

    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            document.getElementById(activeFilter).classList.remove('active');

            activeFilter = this.id;

            this.classList.add('active');

            if (activeFilter === 'filterAll') {
                showAllRows();
            } else if (activeFilter === 'filterIncomplete') {
                hideCompleteRows();
            } else if (activeFilter === 'filterComplete') {
                hideIncompleteRows();
            }
        });
    });

    function showAllRows() {
        Array.from(taskTable.getElementsByTagName('tr')).forEach((row, index) => {
            row.style.display = '';
            row.firstElementChild.innerText = index + 1;
        });
    }

    function hideCompleteRows() {
        Array.from(taskTable.getElementsByClassName('complete-task')).forEach((row, index) => {
            row.style.display = 'none';
            row.firstElementChild.innerText = index + 1;
        });
        Array.from(taskTable.getElementsByClassName('incomplete-task')).forEach((row, index) => {
            row.style.display = '';
            row.firstElementChild.innerText = index + 1;
        });
    }

    function hideIncompleteRows() {
        Array.from(taskTable.getElementsByClassName('incomplete-task')).forEach((row, index) => {
            row.style.display = 'none';
            row.firstElementChild.innerText = index + 1;
        });
        Array.from(taskTable.getElementsByClassName('complete-task')).forEach((row, index) => {
            row.style.display = '';
            row.firstElementChild.innerText = index + 1;
        });
    }
});
