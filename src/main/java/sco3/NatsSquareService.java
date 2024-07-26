package sco3;

import java.nio.ByteBuffer;

import io.nats.client.Connection;
import io.nats.client.Dispatcher;
import io.nats.client.Nats;

public class NatsSquareService implements NatsSquare {
	static int mCnt = 0;

	public static void main(String[] args) throws Exception {
		var buffer = ByteBuffer.allocate(ILEN);
		Connection nc = Nats.connect("nats://localhost:4222");

		Dispatcher d = nc.createDispatcher((msg) -> {
			byte[] inBytes = msg.getData();
			buffer.put(0, inBytes, 0, ILEN);
			int in = buffer.getInt(0);
			int out = in * in;
//			mCnt++;
//			if (mCnt % 1000 == 0) {
//				System.out.println(mCnt);
//			}
			buffer.putInt(0, out);
			buffer.get(0, inBytes, 0, ILEN);
			nc.publish(msg.getReplyTo(), inBytes);
		});
		String queueName = NatsSquareService.class.getName();
		d.subscribe(SQUARE, queueName);

	}

}
