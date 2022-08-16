import com.github.davidmc24.gradle.plugin.avro.GenerateAvroJavaTask
import com.google.protobuf.gradle.proto
import com.google.protobuf.gradle.protobuf
import com.google.protobuf.gradle.protoc

plugins {
    id("java")
    id("application")
    id("idea")

    id("com.github.davidmc24.gradle.plugin.avro-base") version "1.0.0"
    id("com.google.protobuf") version "0.8.15"
}

group = "com.laeith.comp.sci.excursions"
version = "0.1"


repositories {
    gradlePluginPortal()
    mavenCentral()
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(17))
    }
}

val log4jVer = "2.18.0"

val agronaVer = "1.11.0"
val vavrVer = "0.10.4"

val junitVer = "5.8.1"
val mockitoVer = "4.0.0"

val findbugsVer = "3.0.1u2"
val jmhVer = "1.32"
val jolVer = "0.16"

val protobufVer = "3.15.1"
val avroVer = "1.10.2"
val sbeVer = "1.21.0"
val jacksonVer = "1.21.0"
val xmlJacksonVer = "2.12.2"
val woodstoxVer = "5.1.0"
val dslJsonVer = "1.9.8"

val javaAllocationInstrumenter = "3.3.0"
val asmVer = "9.3"
val byteBuddy = "1.12.12"

dependencies {
    implementation("org.apache.logging.log4j:log4j-api:$log4jVer")
    implementation("org.apache.logging.log4j:log4j-core:$log4jVer")

    implementation("org.agrona:agrona:$agronaVer")
    implementation("io.vavr:vavr:$vavrVer")
    implementation("com.google.code.findbugs:annotations:$findbugsVer")

//  Serialization - wire formats
    implementation("com.google.protobuf:protobuf-java:$protobufVer")
    implementation("com.google.protobuf:protobuf-java-util:$protobufVer")
    implementation("org.apache.avro:avro:$avroVer")
    implementation("uk.co.real-logic:sbe-all:$sbeVer")
    implementation("com.fasterxml.jackson.core:jackson-databind:$jacksonVer")
    annotationProcessor("com.dslplatform:dsl-json-java8:$dslJsonVer")
    implementation("com.dslplatform:dsl-json-java8:$dslJsonVer")

    implementation("com.fasterxml.jackson.dataformat:jackson-dataformat-xml:$xmlJacksonVer")
    implementation("com.fasterxml.woodstox:woodstox-core:$woodstoxVer")

//    Memory layout tool
    implementation("org.openjdk.jol:jol-core:$jolVer")

//    Instrumentation / measurements
//    This is a custom build of google/allocation-instrumenter 3.3.0 with upgraded ASM version so that
//    it works for JDK 17 objects
    implementation(files("libs/java-allocation-instrumenter-3.3.ASM.PATCHED.JDK17.jar"))
    implementation("net.bytebuddy:byte-buddy:$byteBuddy")
    implementation("net.bytebuddy:byte-buddy-agent:$byteBuddy")

//    Testing & benchmarking
    testImplementation("org.junit.jupiter:junit-jupiter:$junitVer")
    testImplementation("org.mockito:mockito-core:$mockitoVer")
    testImplementation("org.assertj:assertj-core:3.11.1")

    implementation("org.openjdk.jmh:jmh-core:$jmhVer")
    annotationProcessor("org.openjdk.jmh:jmh-generator-annprocess:$jmhVer")

    protobuf(files("messages/proto/"))
}

sourceSets {
    main {
        proto {
            srcDir("generated/generatedProtobuf")
        }
        java.srcDir("generated")
    }

    test {
        java.srcDir("generated")
    }
}

tasks.getByName<Test>("test") {
    useJUnitPlatform()
}

tasks.register<GenerateAvroJavaTask>("generateAvro") {
    source("messages/avro")
    setOutputDir(File("generated/generatedAvro"))
}

tasks.named("compileJava") {
    dependsOn("deleteGenerated")
    dependsOn("generateAvro")
    dependsOn("generateProto")
    dependsOn("generateSBE")
}

tasks.named("processResources") {
    dependsOn("generateProto")
}

tasks.register<JavaExec>("generateSBE") {
    systemProperties["sbe.output.dir"] = "$projectDir/generated/generatedSBE"
    systemProperties["sbe.target.namespace"] = "com.laeith.playground"

    classpath = sourceSets.main.get().compileClasspath
    main = "uk.co.real_logic.sbe.SbeTool"
    args = listOf("$projectDir/messages/sbe/schema.xml")
}

tasks.register<Delete>("deleteGenerated") {
    delete(files("$projectDir/generated"))
}

protobuf {
    generatedFilesBaseDir = "$projectDir/generated/generatedProtobuf"

    protoc {
        // Will download protoc from a repository and use it
        artifact = "com.google.protobuf:protoc:$protobufVer"
    }
}
