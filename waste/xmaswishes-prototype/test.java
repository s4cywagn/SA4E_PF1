@RunWith(CamelSpringRunner.class) // or @ExtendWith for JUnit 5
@BootstrapWith(SpringBootTestContextBootstrapper.class)
@SpringBootTest
public class ScannedLettersRouteTest {

    @Autowired
    CamelContext camelContext;

    @EndpointInject("mock:http:localhost:3000/wishes")
    protected MockEndpoint mockEndpoint;

    @Test
    public void testFileProcessing() throws Exception {
        // Expect 1 message in the mock endpoint
        mockEndpoint.expectedMessageCount(1);

        // Send a test file message to the direct route:
        // e.g., direct:start or file endpoint in a test folder.
        ProducerTemplate producer = camelContext.createProducerTemplate();
        producer.sendBodyAndHeader("file:data/scanned-letters", 
                                   "This is a scanned letter test",
                                   Exchange.FILE_NAME, "testLetter.txt");

        // Assertions
        mockEndpoint.assertIsSatisfied();
        
        // You can further assert things about the body, headers, etc.
    }
}
