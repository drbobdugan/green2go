import 'package:Choose2Reuse/components/font_scale_blocker.dart';
import 'package:flutter/material.dart';

import '../components/reuse_containerList.dart';
import '../components/reuse_label.dart';
import '../components/reuse_loading.dart';
import '../components/reuse_userBar.dart';
import '../services/api.dart';
import '../services/navigation_service.dart';
import '../services/student_service.dart';
import '../static/container.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/student.dart';

enum FilterOptions { All, CheckedOut, Pending, Verified, DamagedLost }

const List<FilterOptions> items = <FilterOptions>[
  FilterOptions.All,
  FilterOptions.CheckedOut,
  FilterOptions.Pending,
  FilterOptions.Verified,
  FilterOptions.DamagedLost
];

Map<FilterOptions, String> labels = <FilterOptions, String>{
  FilterOptions.All: 'All',
  FilterOptions.CheckedOut: containerLabels[ContainerStatus.CheckedOut],
  FilterOptions.Pending: containerLabels[ContainerStatus.Pending],
  FilterOptions.Verified: containerLabels[ContainerStatus.Verified],
  FilterOptions.DamagedLost: containerLabels[ContainerStatus.DamagedLost]
};

class ContainerListPage extends StatefulWidget {
  const ContainerListPage({Key key, @required this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onGetSortedContainers() async {
    return await StudentService.getSortedContainers(userAuth);
  }

  Future<APIResponse> onSubmitReport(
      ReusableContainer container, String report) async {
    if (container.status == ContainerStatus.DamagedLost) {
      return await StudentService.undoReportContainer(
          userAuth, container.qrCode);
    }
    return await StudentService.reportContainer(
        userAuth, container.qrCode, report);
  }

  @override
  _ContainerListPageState createState() => _ContainerListPageState();
}

class _ContainerListPageState extends State<ContainerListPage> {
  StudentDetails user;
  List<ReusableContainer> filteredContainers;
  String filterOn;

  @override
  void initState() {
    super.initState();

    user = StudentDetails(widget.userAuth);

    widget.onGetSortedContainers().then((APIResponse response) {
      if (response.success) {
        setState(() {
          user.sortedContainers =
              SortedReusableContainers(response.data as Map<String, dynamic>);
          filteredContainers = user.sortedContainers.all;
        });
      }
    });
  }

  void onFilter(String filterName) {
    setState(() {
      filterOn = filterName;
    });
    reFilter();
  }

  void reFilter() {
    setState(() {
      if (filterOn == labels[FilterOptions.CheckedOut]) {
        filteredContainers = user.sortedContainers.checkedOut;
      } else if (filterOn == labels[FilterOptions.Pending]) {
        filteredContainers = user.sortedContainers.pending;
      } else if (filterOn == labels[FilterOptions.Verified]) {
        filteredContainers = user.sortedContainers.verified;
      } else if (filterOn == labels[FilterOptions.DamagedLost]) {
        filteredContainers = user.sortedContainers.damagedLost;
      } else {
        filteredContainers = user.sortedContainers.all;
      }
    });
  }

  void handleSubmitReport(int index, String message) {
    widget
        .onSubmitReport(user.topContainers[index], message)
        .then((APIResponse response) {
      if (response.success) {
        NavigationService(context: context).goHome(widget.userAuth);
      }
    });
    reFilter();
  }

  @override
  Widget build(BuildContext context) {
    if (user.sortedContainers == null) {
      return const Scaffold(
        backgroundColor: Colors.white,
        body: ReuseLoading(),
      );
    }

    return FontScaleBlocker(
      child: Scaffold(
        backgroundColor: Colors.white,
        appBar: UserAppBar(userAuth: widget.userAuth),
        body: SizedBox(
          width: MediaQuery.of(context).size.width,
          height: MediaQuery.of(context).size.height,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: <Widget>[
                  ReuseLabel(
                    text: ReuseStrings.containerListTitle,
                    textStyle: CustomTheme.primaryLabelStyle(),
                    top: 30,
                    left: 10,
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      ReuseLabel(
                        text: ReuseStrings.filterBy,
                        top: 30,
                        textStyle:
                            CustomTheme.secondaryLabelStyle(fontSize: 16.0),
                      ),
                      Padding(
                        padding: const EdgeInsets.fromLTRB(10, 30, 10, 0),
                        child: Container(
                          height: 50.0,
                          width: 50.0,
                          decoration: BoxDecoration(
                              color: CustomTheme.getColor('light'),
                              borderRadius:
                                  const BorderRadius.all(Radius.circular(50))),
                          child: PopupMenuButton<String>(
                            icon: const Icon(Icons.filter_alt,
                                color: Colors.white),
                            onSelected: (String value) {
                              onFilter(value);
                            },
                            itemBuilder: (BuildContext context) {
                              return items.map((FilterOptions option) {
                                return PopupMenuItem<String>(
                                  value: labels[option],
                                  child: Row(
                                    children: <Widget>[
                                      Text(
                                        labels[option],
                                        textScaleFactor: 1,
                                        style: TextStyle(
                                          fontWeight: FontWeight.bold,
                                          color:
                                              CustomTheme.getColor('primary'),
                                        ),
                                      ),
                                    ],
                                  ),
                                );
                              }).toList();
                            },
                          ),
                        ),
                      )
                    ],
                  ),
                ],
              ),
              ReuseContainerList(
                  userAuth: widget.userAuth,
                  containers: filteredContainers,
                  submitReport: handleSubmitReport),
            ],
          ),
        ),
      ),
    );
  }
}
