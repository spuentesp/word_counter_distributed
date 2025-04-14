package WordCounter;
import com.zeroc.Ice.*;

public class Main {
    public static void main(String[] args) {
        try (Communicator communicator = Util.initialize(args)) {
            ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints("WorkerAdapter", "default -p 10000");
            WorkerImpl servant = new WorkerImpl();
            adapter.add(servant, Util.stringToIdentity("JavaWorker"));
            adapter.activate();
            System.out.println(" Java worker iniciado en puerto 10000...");
            communicator.waitForShutdown();
        }
    }
}
