package sco3;

import static java.lang.System.out;

import org.junit.Assert;
import org.junit.Test;

public class DevTestMany {

	public static class Wrapper {
		String mName = "";

		public Wrapper(String s) {
			mName = s;
		}

		@Override
		public String toString() {
			return mName;
		}

		@Override
		public void finalize() {
			out.println("Finalize: " + mName);
		}
	}

	@Test
	public void test() {

		int i = 0;
		while (true) {
			Wrapper s = new Wrapper("Asdf" + i);
			Assert.assertNotNull(s);
			i++;
			out.println(s);
		}
	}

}
