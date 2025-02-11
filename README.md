# **Assignment: Development of a Retrieval Augmented Generation Application**

## **Submission Due:**  
📅 **February 26, 2025, 11:59 PM**  

## **Objective**  
Develop a **Retrieval Augmented Generation (RAG) application** that enables users to upload documents and interact with their content through a **conversational interface**. The application should efficiently handle large files by **breaking them into smaller chunks** and support **multiple file formats** and **multiple document uploads**.

---

## **Provided Resources**  
📦 **Development Template:**  
A template is provided, including **Docker** and **.devcontainer** configurations to streamline your development environment.

---

## **Requirements (Total: 200 points)**  

### **1. Utilize the Provided Docker and Devcontainer Setup (10 points)**  
✅ **Description:**  
Use the provided template with **Docker** and **.devcontainer** configurations for your application development. Ensure your application runs successfully within this environment.  

📌 **Deliverables:**  
- Any **necessary modifications** to the Docker or Devcontainer configurations should be documented.  
- **Instructions** in your `README.md` on how to run the application using the provided setup.  

---

### **2. File Upload Functionality for .txt Files (10 points)**  
✅ **Description:**  
Implement functionality that allows users to upload **text files (`.txt` extension)**.  

📌 **Deliverables:**  
- A **user interface component** that enables file selection and uploading.  
- **Backend handling** of the uploaded `.txt` files.  

---

### **3. Conversational Interface with Document Content (150 points)**  
✅ **Description:**  
Create a **chat interface** where users can ask questions about the uploaded document(s) and receive **relevant answers**.  

📌 **Specifications:**  
- Efficiently handle **large documents** by **chunking** them into smaller, manageable pieces.  
- Ensure the **conversational AI** provides **accurate and contextually relevant responses**.  
- Implement **retrieval mechanisms** to fetch information from the document chunks.  

📌 **Deliverables:**  
- A **fully functional chat interface** integrated into your application.  
- **Backend logic** for processing user queries and retrieving relevant information from the documents.  

---

### **4. Support for .txt and .pdf File Formats (15 points)**  
✅ **Description:**  
Extend the **file upload functionality** to accept both **`.txt` and `.pdf`** files.  

📌 **Deliverables:**  
- Updated **file upload component** that allows selection of `.txt` and `.pdf` files.  
- Implementation of **PDF parsing** to extract text content for processing.  

---

### **5. Ability to Add Multiple Documents (15 points)**  
✅ **Description:**  
Allow users to upload **multiple documents** and interact with all of them within the chat interface.  

📌 **Deliverables:**  
- Modified **upload system** to handle multiple files.  
- Logic to **manage and differentiate content** from multiple documents during conversations.  

---

## **Submission Guidelines**  

📂 **Code Repository:**  
- Submit your code via a **Git repository** (e.g., GitHub, GitLab) or upload a `.zip` file.  
- Ensure **no secret keys** are submitted.  

📜 **README File (Must Include):**  
- **Instructions** on how to run your application using the **provided Docker and Devcontainer setup**.  
- **Overview of your application’s features**.  
- **Documentation of any changes** made to the provided configurations.  

📌 **Documentation:**  
- Ensure your **code is well-documented** with comments.  
- Follow **best coding practices**.  
- _(Hint: After finishing your work, test the project on a computer without your development environment to ensure it runs successfully.)_  

---

## **Additional Notes**  
💡 **User Experience:**  
- Focus on creating an **intuitive and user-friendly** interface.  

⚠ **Academic Integrity:**  
- Ensure all work submitted is **your own**.  
- Properly **cite any external resources** used.  
