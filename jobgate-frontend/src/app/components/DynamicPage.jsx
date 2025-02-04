// src/app/about/[id]/page.jsx
const DynamicPage = async ({ params }) => {
    const { id } = await params;
    
    // Now you can use await for any async operations
    // Example:
    // const data = await fetchSomeData(id);
  
    return (
      <div>
        <h1>Dynamic Page</h1>
        <p>The dynamic ID is: {id}</p>
      </div>
    );
};
  
export default DynamicPage;