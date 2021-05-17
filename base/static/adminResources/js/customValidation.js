

function addComplain() {

	if ($('#complaintSubject').val().trim() === '') {
		$('#complaintSubject').focus()
		showErrorToast('Please select complain  type')
		return false;
	} else if ($('#complaintDescription').val().trim() === '') {
		$('#complaintDescription').focus()
		showErrorToast('Please enter dis of table')
		return false;
	}else {
		return true;
	}
}


function addDataset() {

	if ($('#datasetImage').val().trim() === '') {
		$('#datasetImage').focus()
		showErrorToast('Please select image type')
		return false;
	} else if ($('#datasetDescription').val().trim() === '') {
		$('#datasetDescription').focus()
		showErrorToast('Please enter dis of table')
		return false;
	}else {
		return true;
	}
}
