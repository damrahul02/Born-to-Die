<?php
// Database connection
include('connection.php');

// Check if form is submitted
if (isset($_POST['apply'])) {
    $application_id = $_POST['application_id'];

    // Fetch vaccine status
    $statusSql = "SELECT status FROM vaccine_status WHERE application_id = ?";
    $stmt = $conn->prepare($statusSql);
    $stmt->bind_param('i', $application_id);
    $stmt->execute();
    $statusResult = $stmt->get_result()->fetch_assoc();

    if ($statusResult['status'] == 1) {
        // Generate birth certificate
        generateBirthCertificate($application_id);
    } else {
        echo "Your birth certificate is not ready yet, complete all the doses of the vaccine.";
    }
}

function generateBirthCertificate($application_id) {
    // Fetch applicant details
    global $conn;
    $applicantSql = "SELECT * FROM applicants WHERE application_id = ?";
    $stmt = $conn->prepare($applicantSql);
    $stmt->bind_param('i', $application_id);
    $stmt->execute();
    $applicant = $stmt->get_result()->fetch_assoc();

    // Create PDF (you can use a library like FPDF or TCPDF)
    require('fpdf/fpdf.php');
    $pdf = new FPDF();
    $pdf->AddPage();
    $pdf->SetFont('Arial', 'B', 16);
    $pdf->Cell(0, 10, 'Birth Certificate', 0, 1, 'C');
    $pdf->Ln(10);

    // Add applicant details
    $pdf->SetFont('Arial', '', 12);
    $pdf->Cell(0, 10, 'Full Name: ' . $applicant['full_name']);
    $pdf->Ln();
    $pdf->Cell(0, 10, 'Gender: ' . $applicant['gender']);
    $pdf->Ln();
    $pdf->Cell(0, 10, 'Date of Birth: ' . $applicant['birth_date']);
    $pdf->Ln();
    $pdf->Cell(0, 10, 'Birthplace: ' . $applicant['birth_country']);
    $pdf->Ln();
    // Add more details as needed

    $pdf->Output('I', 'Birth_Certificate_' . $application_id . '.pdf');
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Apply for Birth Certificate</title>
</head>
<body>
    <form method="post" action="">
        <label for="application_id">Application ID:</label>
        <input type="text" id="application_id" name="application_id" required>
        <button type="submit" name="apply">Apply for Birth Certificate</button>
    </form>
</body>
</html>
