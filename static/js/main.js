// fetch(
//   "https://dummyjson.com/books/?limit=10&skip=5&select=key1&select=key2&select=key3",
//   {
//     method: "GET",
//   }
// )
//   .then((data) => data.json())
//   .then((allBooks) => {
//     renderBooks(allBooks);
//   });

// const initialBooks = [
//   {
//     id: 1,
//     title: "The Alchemist",
//     author: "Paulo Coelho",
//   },
// ];

// // renderBooks(initialBooks);

// function renderBooks(books) {
//   // add the book to the table
//   books.forEach((book, idx) => {
//     const table = document.getElementById("book_table");
//     const row = document.createElement("tr");
//     row.innerHTML = `
//   <th>${idx}</th>
// <td>${book.title}</td>
// <td>${book.author}</td>
// <td>
// `;
//     table.appendChild(row);
//   });
// }
// // Select all forms
// const forms = {
//   bookAddForm: document.getElementById("book_add_form"),
//   authorAddForm: document.getElementById("author_add_form"),
//   publisherAddForm: document.getElementById("publisher_add_form"),
//   customerAddForm: document.getElementById("customer_add_form"),
//   ordersAddForm: document.getElementById("orders_add_form"),
//   orderedBooksAddForm: document.getElementById("ordered_books_add_form"),
// };

// // Add event listeners to all forms
// Object.values(forms).forEach((form) => {
//   if (form) {
//     form.addEventListener("submit", (e) => handleSubmit(e, form.id));
//   }
// });

// // Centralized form submission handler
// async function handleSubmit(e, formId) {
//   e.preventDefault();

//   // Prepare form data
//   const formData = new FormData(e.target);
//   const data = Object.fromEntries(formData.entries());

//   console.log(`[${formId}] Submitted Data:`, data);

//   // Map form IDs to API endpoints
//   const apiEndpoints = {
//     book_add_form:
//       "https://bookstoreappapi.herokuapp.com/api/v1/bookstore/books",
//     author_add_form:
//       "https://bookstoreappapi.herokuapp.com/api/v1/bookstore/authors",
//     publisher_add_form:
//       "https://bookstoreappapi.herokuapp.com/api/v1/bookstore/publishers",
//     customer_add_form:
//       "https://bookstoreappapi.herokuapp.com/api/v1/bookstore/customers",
//     orders_add_form:
//       "https://bookstoreappapi.herokuapp.com/api/v1/bookstore/orders",
//     ordered_books_add_form:
//       "https://bookstoreappapi.herokuapp.com/api/v1/bookstore/ordered-books",
//   };

//   const apiUrl = apiEndpoints[formId];
//   if (!apiUrl) {
//     alert(`No API endpoint mapped for form ID: ${formId}`);
//     return;
//   }

//   try {
//     // Submit the data to the API
//     const response = await fetch(apiUrl, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(data),
//     });

//     // Handle API response
//     if (response.ok) {
//       const responseData = await response.json();
//       console.log(`[${formId}] API Response:`, responseData);
//       alert("Data added successfully!");
//       e.target.reset(); // Reset the form after successful submission
//     } else {
//       const errorData = await response.json();
//       console.error(`[${formId}] API Error:`, errorData);
//       alert(`Failed to add data: ${errorData.message || "Unknown error"}`);
//     }
//   } catch (error) {
//     console.error(`[${formId}] Network Error:`, error);
//     alert("An error occurred while submitting the form. Please try again.");
//   }
// }

// function deleteBook(id) {
//   fetch(`https://bookstoreappapi.herokuapp.com/api/v1/bookstore/books/${id}`, {
//     method: "DELETE",
//   });
// }
