package com.laeith.com.sci.excursions.utils.instrumentation;

import com.google.monitoring.runtime.instrumentation.AllocationRecorder;
import com.google.monitoring.runtime.instrumentation.Sampler;
import com.laeith.com.sci.excursions.utils.StackTrace;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

public class DefaultAllocationSampler {
  
  private static final Map<StackTrace, List<MemoryAllocationRecord>> stackToRecordsMap = new HashMap<>();
  // TODO: Marcin: Consider AtomicCounter instead of AtomicLong
  private static final Map<StackTrace, AtomicLong> stackTraceAllocationCounter = new HashMap<>();
  
  private static final Sampler allocationSampler = (count, desc, newObj, size) -> {
    if (desc.startsWith("com/google/monitoring/runtime/instrumentation") ||
        desc.startsWith("org/junit/platform")) {
      return; // Don't record auxiliary allocations
    }
    
    // TODO: Marcin: Would be nice to add stacktrace modifications so that it omits instrumentation-related parts
    var st = StackTrace.forThread(Thread.currentThread());
    var allocationRecord = new MemoryAllocationRecord(desc, count, newObj, size, st);
    
    stackToRecordsMap.getOrDefault(st, new ArrayList<>()).add(allocationRecord);
    stackTraceAllocationCounter.getOrDefault(st, new AtomicLong(0)).incrementAndGet();
    
    System.out.printf("Allocated %s with %s count of size %s for: %s%n", desc, count, size, newObj);
    st.printStackTrace(System.out);
    //  For an 'asserting' implementation we could throw an exception here to make sure nothing is allocated
  };
  
  public static void start() {
    AllocationRecorder.addSampler(allocationSampler);
  }
  
  public static void stop() {
    AllocationRecorder.removeSampler(allocationSampler);
  }
  
  public static void prettyPrintSummary() {
    throw new UnsupportedOperationException("Not implemented yet");
  }
  
}
