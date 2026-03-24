import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:sizer/sizer.dart'; // تأكد من وجودها في pubspec
import 'package:vortex_market/logic/login_bloc/auth_bloc/auth_bloc.dart';
import 'presentation/screens/auth/login_screen.dart'; // المسار الجديد الصحيح

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // نستخدم Sizer لجعل التصميم متجاوب مع كل الشاشات
    return Sizer(
      builder: (context, orientation, deviceType) {
        return BlocProvider(
          // نوفر AuthBloc على مستوى التطبيق ليكون متاحاً لجميع الشاشات
          create: (context) => AuthBloc(),
          child: MaterialApp(
            title: 'Vortex Market',
            debugShowCheckedModeBanner: false,
            theme: ThemeData(
              primarySwatch: Colors.purple,
              useMaterial3: true,
              brightness: Brightness.dark, // ليتناسب مع النمط الزجاجي الداكن
            ),
            home: LoginScreen(), // استدعاء الشاشة بالاسم الصحيح
          ),
        );
      },
    );
  }
}
