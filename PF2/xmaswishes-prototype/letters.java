import org.apache.camel.builder.RouteBuilder;
import org.springframework.stereotype.Component;

@Component
public class ScannedLettersRoute extends RouteBuilder {

    @Override
    public void configure() throws Exception {

        // 1) File-Endpoint: Überwacht das Verzeichnis "data/scanned-letters"
        from("file:data/scanned-letters?noop=true")
            // 2) Loggen, dass wir eine Datei gefunden haben
            .log("New scanned letter file: ${header.CamelFileName}")
            // 3) Processor, der den Brief-Inhalt aufbereitet (z.B. OCR, Parsing)
            .process(exchange -> {
                // Hier könntest du den Dateicontent lesen und verarbeiten
                String fileContent = exchange.getIn().getBody(String.class);
                // Evtl. OCR-Aufruf, Regex, JSON-Erzeugung etc.
                // Simulation: Wir bauen einfach einen JSON-String:
                String requestBody = "{ \"text\": \"" + fileContent.replace("\n"," ") + "\" }";
                exchange.getIn().setBody(requestBody);
            })
            // 4) Sende POST-Request an XmasWishes-System
            .to("http://localhost:3000/wishes?httpMethod=POST")
            // 5) Abschließendes Log
            .log("Letter sent to XmasWishes. Response: ${body}");
    }
}
