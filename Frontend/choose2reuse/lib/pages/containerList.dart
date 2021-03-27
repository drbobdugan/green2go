import 'package:flutter/material.dart';

import '../components/reuse_label.dart';
import '../components/reuse_loading.dart';
import '../components/reuse_userBar.dart';
import '../services/api.dart';
import '../services/student_service.dart';
import '../static/container.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/student.dart';

enum FilterOptions { All, CheckedOut, Pending, Verified }

const List<FilterOptions> items = <FilterOptions>[
  FilterOptions.All,
  FilterOptions.CheckedOut,
  FilterOptions.Pending,
  FilterOptions.Verified
];

const Map<FilterOptions, String> labels = <FilterOptions, String>{
  FilterOptions.All: 'All',
  FilterOptions.CheckedOut: 'Checked Out',
  FilterOptions.Pending: 'Pending Return',
  FilterOptions.Verified: 'Verified Return'
};

class ContainerListPage extends StatefulWidget {
  const ContainerListPage({Key key, @required this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onGetSortedContainers() async {
    return await StudentService.getSortedContainers(userAuth);
  }

  @override
  _ContainerListPageState createState() => _ContainerListPageState();
}

class _ContainerListPageState extends State<ContainerListPage> {
  StudentDetails user;
  List<ReusableContainer> filteredContainers;

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

  ListView getContainerDataLarge() {
    return ListView.builder(
      itemCount: filteredContainers.length,
      itemBuilder: (BuildContext context, int index) {
        final ReusableContainer container = filteredContainers[index];
        return Padding(
          padding: const EdgeInsets.only(top: 30.0),
          child: container.dataRow(),
        );
      },
    );
  }

  void onFilter(String filterOn) {
    setState(() {
      if (filterOn == labels[FilterOptions.CheckedOut]) {
        filteredContainers = user.sortedContainers.checkedOut;
      } else if (filterOn == labels[FilterOptions.Verified]) {
        filteredContainers = user.sortedContainers.verified;
      } else if (filterOn == labels[FilterOptions.Pending]) {
        filteredContainers = user.sortedContainers.unverified;
      } else {
        filteredContainers = user.sortedContainers.all;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (user.sortedContainers == null) {
      return const Scaffold(
        backgroundColor: Colors.white,
        body: ReuseLoading(),
      );
    }

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: UserAppBar(userAuth: widget.userAuth),
      body: SizedBox(
        width: MediaQuery.of(context).size.width,
        height: MediaQuery.of(context).size.height,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: <
                Widget>[
              SizedBox(
                  height: 75,
                  width: MediaQuery.of(context).size.width - 130,
                  child: ReuseLabel(
                      text: ReuseStrings.containerListTitle,
                      textStyle: CustomTheme.primaryLabelStyle(),
                      top: 30.0,
                      bottom: 15.0)),
              Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: <
                  Widget>[
                ReuseLabel(
                  text: ReuseStrings.filterBy,
                  textStyle: CustomTheme.secondaryLabelStyle(fontSize: 16.0),
                  right: 10.0,
                ),
                Container(
                    height: 50.0,
                    width: 100.0,
                    decoration: BoxDecoration(
                        color: CustomTheme.getColor('light'),
                        borderRadius:
                            const BorderRadius.all(Radius.circular(50))),
                    child: PopupMenuButton<String>(
                      icon: const Icon(Icons.filter_alt, color: Colors.white),
                      onSelected: (String value) {
                        onFilter(value);
                      },
                      itemBuilder: (BuildContext context) {
                        return items.map((FilterOptions option) {
                          return PopupMenuItem<String>(
                              value: labels[option],
                              child: Row(children: <Widget>[
                                Text(labels[option],
                                    style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        color: CustomTheme.getColor('primary')))
                              ]));
                        }).toList();
                      },
                    ))
              ])
            ]),
            Expanded(
              child: getContainerDataLarge(),
            )
          ],
        ),
      ),
    );
  }
}
