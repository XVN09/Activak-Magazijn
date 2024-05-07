import 'dart:async';
import '/actions/actions.dart' as action_blocks;
import 'package:flutter/material.dart';

Future generateNumber(BuildContext context) async {
  unawaited(
    () async {
      await action_blocks.generateNumber(context);
    }(),
  );
}
