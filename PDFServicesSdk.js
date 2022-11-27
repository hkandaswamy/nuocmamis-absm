/* Vanessa Lee | CSC 191
This is the start of the API connection for Adobe PDF Services to convert static HTML form pages to PDF */

const PDFServicesSdk = require('@adobe/pdfservices-node-sdk');

 const setCustomOptions = (htmlToPDFOperation) => {
   // Define the page layout, in this case an 8 x 11.5 inch page (effectively portrait orientation).
   const pageLayout = new PDFServicesSdk.CreatePDF.options.PageLayout();
   pageLayout.setPageSize(8, 11.5);

   // Set the desired HTML-to-PDF conversion options.
   const htmlToPdfOptions = new PDFServicesSdk.CreatePDF.options.html.CreatePDFFromHtmlOptions.Builder()
     .includesHeaderFooter(true)
     .withPageLayout(pageLayout)
     .build();
   htmlToPDFOperation.setOptions(htmlToPdfOptions);
 };


 try {
   // Initial setup, create credentials instance.
   const credentials =  PDFServicesSdk.Credentials
     .serviceAccountCredentialsBuilder()
     .fromFile("pdfservices-api-credentials.json")
     .build();

   // Create an ExecutionContext using credentials and create a new operation instance.
   const executionContext = PDFServicesSdk.ExecutionContext.create(credentials),
     htmlToPDFOperation = PDFServicesSdk.CreatePDF.Operation.createNew();

   // Set operation input from a source file.
   const input = PDFServicesSdk.FileRef.createFromLocalFile('resources/createPDFFromStaticHtmlInput.zip');
   htmlToPDFOperation.setInput(input);

   // Provide any custom configuration options for the operation.
   setCustomOptions(htmlToPDFOperation);

   // Execute the operation and Save the result to the specified location.
   htmlToPDFOperation.execute(executionContext)
     .then(result => result.saveAsFile('output/createPdfFromStaticHtmlOutput.pdf'))
     .catch(err => {
       if(err instanceof PDFServicesSdk.Error.ServiceApiError
         || err instanceof PDFServicesSdk.Error.ServiceUsageError) {
         console.log('Exception encountered while executing operation', err);
       } else {
         console.log('Exception encountered while executing operation', err);
       }
     });
 } catch (err) {
   console.log('Exception encountered while executing operation', err);
 }

