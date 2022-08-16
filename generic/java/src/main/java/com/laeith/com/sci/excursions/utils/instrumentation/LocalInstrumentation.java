package com.laeith.com.sci.excursions.utils.instrumentation;

import com.google.monitoring.runtime.instrumentation.AllocationInstrumenter;
import com.google.monitoring.runtime.instrumentation.AllocationRecorder;
import net.bytebuddy.agent.ByteBuddyAgent;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.lang.instrument.Instrumentation;
import java.lang.instrument.UnmodifiableClassException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;

public class LocalInstrumentation {
  private static final Logger log = LogManager.getLogger(LocalInstrumentation.class);
  
  private static volatile Instrumentation INST;
  
  public static Instrumentation getInstrumentation() {
    if (INST != null) {
      return INST;
    }
    throw new IllegalStateException("Must call .init() before instrumentation is present");
  }
  
  /**
   * Self-attaches a local Java agent, provides Instrumentation instance for wider project usage and
   * <p>
   * Unfortunately, it's quite hard to get Instrumentation instance without attaching external Java Agents
   * and self-attachment is tricky, ByteBuddyAgent is used to rectify it.
   */
  public static synchronized void init() {
    if (INST == null) {
      ByteBuddyAgent.install();
      INST = ByteBuddyAgent.getInstrumentation();
      
      setupMemoryInstrumentation(INST);
    } else {
      // TODO: Marcin: Save stacktrace?
      log.warn("LocalInstrumentation.init() was called redundantly.");
    }
  }
  
  /**
   * Instead o writing custom allocation instrumentation we want to leverage google/allocation-instrumenter
   * but it wasn't necessarily built with self-attachment in mind (with good reasons), this meant that
   * it had to be hacked a little as per below.
   * <p>
   * // TODO: Marcin: Investigate JEP-331 as an alternative method for allocation profiling
   */
  private static synchronized void setupMemoryInstrumentation(Instrumentation inst) {
    // Preload required classes by AllocationInstrumenter to avoid circular dependency
    try {
      Class.forName("sun.security.provider.PolicyFile");
      Class.forName("java.util.ResourceBundle");
      Class.forName("java.util.Date");
    } catch (Throwable t) {
      // NOP
    }
    
    try {
      // Inject Instrumentation using reflection as the usual premain() method doesn't really work for
      // self-attached agents
      final Field arInst = AllocationRecorder.class.getDeclaredField("instrumentation");
      arInst.setAccessible(true);
      assert arInst.get(null) == null;
      arInst.set(null, inst);
      
      var bootstrapMethod = AllocationInstrumenter.class.getDeclaredMethod("bootstrap", Instrumentation.class);
      bootstrapMethod.setAccessible(true);
      bootstrapMethod.invoke(null, inst);
      
    } catch (NoSuchFieldException | IllegalAccessException | NoSuchMethodException | InvocationTargetException e) {
      throw new RuntimeException(e);
    }
    
    try {
      inst.retransformClasses(Object.class);
    } catch (UnmodifiableClassException e) {
      log.error("LocalInstrumenter was unable to retransform java.lang.Object.");
    }
    
    // Get the set of already loaded classes that can be rewritten.
    Class<?>[] classes = inst.getAllLoadedClasses();
    ArrayList<Class<?>> classList = new ArrayList<>();
    for (Class<?> aClass : classes) {
      if (inst.isModifiableClass(aClass) &&
          aClass != Object.class &&
          !isExcludedFromRetranformation(aClass)) {
        classList.add(aClass);
      }
    }
    
    // Reload classes, if possible.
    Class<?>[] workaround = new Class<?>[classList.size()];
    
    try {
      inst.retransformClasses(classList.toArray(workaround));
    } catch (UnmodifiableClassException e) {
      log.error("LocalInstrumenter was unable to retransform early loaded classes.");
    }
  }
  
  private static boolean isExcludedFromRetranformation(Class<?> aClass) {
    var fullName = aClass.getName();
    
    // Ignore auxiliary packages/libraries that have issues when used from self-attached agent
    // and we now of their garbage-hostile nature.
    if (fullName.startsWith("org.apache.logging.log4j")) {
      return true;
    }
    
    return false;
  }
  
}
